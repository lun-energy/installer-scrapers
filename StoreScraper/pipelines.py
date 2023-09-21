# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class StoreScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['Source'] = spider.name

        if adapter.get('Name1') is None:
            raise DropItem(f'Missing Name1')

        if adapter.get('Address') is None:
            raise DropItem(f'Missing Address')

        if adapter.get('Email'):
            adapter['EmailDomain'] = adapter['Email'].split('@')[1]

        full_name = f'{adapter.get("Name1")} {adapter.get("Name2")}'.upper()
        adapter['Gmbh'] = 'GMBH' in full_name

        return item
