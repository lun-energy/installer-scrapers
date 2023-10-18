import json

from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class DvienergiDkSpider(base_spider.BaseSpider):
    name = "dvienergi.com"
    country = 'DK'
    start_urls = ['https://www.dvienergi.com/forhandlere/']

    def parse(self, response: Response, **kwargs):

        marker_list = json.loads(response.xpath('//input[contains(@class, "__markerList")]/@value').get())
        marker_dict = {str(marker['Id']): (marker['Lat'], marker['Lng']) for marker in marker_list}
        for result in response.xpath('//div[contains(@id, "__markerLink")]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)

            item_loader.add_xpath('Name1', './/h4/text()')

            p_nodes = result.xpath('.//div[normalize-space(@class)="mt-4"]/preceding-sibling::p/text()').getall()
            if len(p_nodes) != 2:
                raise Exception('address parsing failed')

            street, postal_code, city = self.parse_address(','.join(p_nodes))
            item_loader.add_value('Address', street)
            item_loader.add_value('City', city)
            item_loader.add_value('Zip', postal_code)

            item_loader.add_xpath('Email', './/a[contains(@href, "mailto:")]/@href')
            item_loader.add_xpath('Website', './/a[normalize-space(@target)="_blank"]/@href')
            item_loader.add_xpath('Phone', './/a[contains(@href, "tel:")]/@href')

            marker_id = result.xpath('@id').get().split('_')[-1].replace('markerLink', '')
            latitude, longitude = marker_dict[marker_id]
            item_loader.add_value('Latitude', latitude)
            item_loader.add_value('Longitude', longitude)

            parsed_result = item_loader.load_item()
            yield self.add_unique_address_id(parsed_result)
