from scrapy import Request, FormRequest
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider
from urllib.parse import urlencode


class ViessmannSpider(base_spider.BaseSpider):
    name = "viessmann.de"

    def start_requests(self):

        for lat, lng in self.calculate_coordinates(radius=25):
            params = {
                'locale': 'de-DE',
                'lat': lat,
                'lng': lng,
                'count': '100',
                'lookupAddress': 'false',
                'skill': 'HEATPUMP'
            }
            yield Request(url='https://api.viessmann.com/dealer-locator/dealer-search/api/dealer/nearby/latlng?' + urlencode(params))

    def parse(self, response: Response, **kwargs):
        for result in response.jmespath('dealers[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.viessmann.de/de/partner-vor-ort-suche.html')
            item_loader.add_jmes('Name1', 'name')

            item_loader.add_jmes('Address', 'address.street')
            item_loader.add_jmes('City', 'address.city')
            item_loader.add_jmes('Zip', 'address.postcode')
            item_loader.add_jmes('Email', 'contact.mail')
            item_loader.add_jmes('Website', 'contact.homepage')
            item_loader.add_jmes('Phone', 'contact.phone')

            item_loader.add_jmes('Latitude', 'position.y')
            item_loader.add_jmes('Longitude', 'position.x')

            parsed_result = item_loader.load_item()
            yield parsed_result
