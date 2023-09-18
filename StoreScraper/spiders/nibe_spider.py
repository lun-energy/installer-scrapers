import re

from scrapy import Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class NibeSpider(base_spider.BaseSpider):
    name = "nibe.eu"

    start_urls = ['https://www.nibe.eu/de-de/suchen--finden/nibe-partner-finden']

    def parse(self, response: Response, **kwargs):
        json_data = re.search('var installers =(.+?)</script>', response.text).group(1)
        json_selector = Selector(text=json_data)
        for result in json_selector.jmespath('[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.nibe.eu/de-de/suchen--finden/nibe-partner-finden')

            item_loader.add_jmes('Name1', 'name')
            item_loader.add_jmes('Name2', 'name2')
            item_loader.add_jmes('Address', 'address.street')
            item_loader.add_jmes('City', 'address.city')
            item_loader.add_jmes('Zip', 'address.zip')
            item_loader.add_jmes('Email', 'email')
            item_loader.add_jmes('Website', 'url')
            item_loader.add_jmes('Phone', 'phone')

            geocode = result.jmespath('geometry.coordinates').getall()
            if len(geocode) == 2:
                item_loader.add_value('Latitude', geocode[0])
                item_loader.add_value('Longitude', geocode[1])

            parsed_result = item_loader.load_item()
            yield parsed_result
