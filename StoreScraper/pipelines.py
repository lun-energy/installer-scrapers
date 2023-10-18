# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

import phonenumbers
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class StoreScraperPipeline:

    @staticmethod
    def format_phone(input_string: str, country: str) -> str:
        formatted_string = re.sub('[^0-9()+-]', '', input_string)
        if not formatted_string:
            return ''
        try:
            parsed_phone = phonenumbers.parse(input_string, country)
            formatted_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.RFC3966).replace('tel:', '')
            return formatted_number
        except:
            return ''

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['Source'] = spider.name

        if adapter.get('Name1') is None:
            raise DropItem(f'Missing Name1')

        if adapter.get('Address') is None:
            raise DropItem(f'Missing Address')

        if adapter.get('Email'):
            adapter['EmailDomain'] = adapter['Email'].split('@')[1]

        phone = adapter.get('Phone')
        if phone:
            adapter['Phone'] = self.format_phone(phone, spider.country)

        full_name = f'{adapter.get("Name1")} {adapter.get("Name2")}'.upper()
        adapter['Gmbh'] = 'GMBH' in full_name

        return item
