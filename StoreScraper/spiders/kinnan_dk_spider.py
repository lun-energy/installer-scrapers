import json
import re

from scrapy import Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem, format_whitespaces
from StoreScraper.spiders import base_spider


class KinnanDkSpider(base_spider.BaseSpider):
    name = "kinnan.dk"
    country = 'DK'
    start_urls = ['https://www.kinnan.dk/mitsubishi-electric-forhandler-luft-vand/']

    def parse(self, response: Response, **kwargs):

        email_regex = re.compile("([a-zA-Z0-9_{|}~-]+(?:\.[a-zA-Z0-9_{|}~-]+)*(@)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9]){2,}?(\.))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)")

        json_data = re.search(r'\.maps\((.+)\)\.data', response.text).group(1)

        for result in json.loads(json_data)['places']:

            item_loader = ItemLoader(item=StoreItem(), selector=result)

            full_address = result['address'].replace(', Denmark', '')

            street, postal_code, city = self.parse_address(full_address)

            if not street:
                street = full_address

            postal_code = result['location']['postal_code'] if postal_code == '' else postal_code
            city = result['location']['city'] if city == '' else city

            item_loader.add_value('Name1', result['title'])
            item_loader.add_value('Address', street)
            item_loader.add_value('Zip', postal_code)
            item_loader.add_value('City', city)

            item_loader.add_value('Latitude', result['location']['lat'])
            item_loader.add_value('Longitude', result['location']['lng'])

            email_match = email_regex.search(result['content'].lower())
            email = email_match.group(1) if email_match is not None else ''
            item_loader.add_value('Email', email)

            content_selector = Selector(text=result['content'].replace('\r\n', '<br />').replace('eller', '<br />').replace(' / ', '<br />'))
            item_loader.add_value('Website', content_selector.css('a::attr(href)').get())

            text_nodes = [format_whitespaces(text).lower() for text in content_selector.xpath('//text()').getall()]
            phone_prefixes = ['tlf', 'telefon']
            phone = [text.replace(prefix, '', 1) for text in text_nodes for prefix in phone_prefixes if text.startswith(prefix)]
            item_loader.add_value('Phone', phone)

            parsed_result = item_loader.load_item()

            yield self.add_unique_address_id(parsed_result)
