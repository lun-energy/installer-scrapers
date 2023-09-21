import re

from scrapy import FormRequest
from scrapy.http import Response

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class PanasonicSpider(base_spider.BaseSpider):
    name = "panasonicproclub.com"

    def start_requests(self):
        post_data = {
            'geo': '0',
            'lat': '51.165691',
            'lng': '10.451526',
            'address': 'Deutschland',
            'selected_list': '36',
            'distance': '500',
            'search': ''
        }
        yield FormRequest(url='https://www.panasonicproclub.com/ifinder/DE_de/home/', formdata=post_data)

    def parse(self, response: Response, **kwargs):
        values = re.findall(r'marcadores\[(\d+)]\[(\d+)]\s*=\s*"(.*?)";', response.text)
        results = dict()
        for row_index, column_index, value in values:
            if row_index not in results:
                results[row_index] = {
                    'Source': self.name
                }
            if column_index == '0':
                results[row_index]['Name1'] = value
            if column_index == '1':
                results[row_index]['Address'] = value
            if column_index == '99':
                results[row_index]['Zip'] = value
            if column_index == '100':
                results[row_index]['City'] = value
            if column_index == '3':
                results[row_index]['Phone'] = value
            if column_index == '4':
                results[row_index]['Email'] = value
            if column_index == '5':
                results[row_index]['Website'] = value
            if column_index == '6':
                results[row_index]['Latitude'] = value
            if column_index == '7':
                results[row_index]['Longitude'] = value
        for key, value in results.items():
            parsed_result = StoreItem(**value)
            yield self.add_unique_address_id(parsed_result)
