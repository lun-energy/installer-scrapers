from urllib.parse import urlencode

from haversine import inverse_haversine, Direction
from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class VaillantSpider(base_spider.BaseSpider):
    name = "vaillant.de"

    @staticmethod
    def point_to_string(coord_tuple: tuple[float, float]) -> str:
        return f'{coord_tuple[0]},{coord_tuple[1]}'

    def start_requests(self):
        radius = 100
        for coord in self.calculate_coordinates(radius=radius):
            sw = inverse_haversine(coord, distance=radius, direction=Direction.SOUTHWEST)
            ne = inverse_haversine(coord, distance=radius, direction=Direction.NORTHEAST)
            params = {
                'qualifications': '1004',
                'c': self.point_to_string(coord),
                'sw': self.point_to_string(sw),
                'ne': self.point_to_string(ne),

            }
            yield Request(url='https://www.vaillant.de/heizung/heizung-finden/partner-finden/?' + urlencode(params))

    def parse(self, response: Response, **kwargs):

        for result in response.xpath('//div[@data-partnersearch-id]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.vaillant.de/heizung/heizung-finden/partner-finden/?qualifications=1004')
            item_loader.add_xpath('Name1', './/h3[@data-partnersearch-company]/text()')
            item_loader.add_xpath('Email', './/li[@data-partnersearch-email]//text()')
            item_loader.add_xpath('Website', './/li[@data-partnersearch-website]//text()')
            item_loader.add_xpath('Phone', './/li[@data-partnersearch-phone]//text()')
            item_loader.add_xpath('Latitude', '@data-partnersearch-lat')
            item_loader.add_xpath('Longitude', '@data-partnersearch-lng')

            address = result.xpath('.//div[@data-partnersearch-address]/text()').get()

            street, postal_code, city = self.parse_address(address)

            item_loader.add_value('Address', street)
            item_loader.add_value('City', city)
            item_loader.add_value('Zip', postal_code)

            parsed_result = item_loader.load_item()
            yield parsed_result
