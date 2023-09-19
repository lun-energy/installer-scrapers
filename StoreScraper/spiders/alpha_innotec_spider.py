import re

from scrapy import Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class AlphaInnotecSpider(base_spider.BaseSpider):
    name = "alpha-innotec.com"

    start_urls = ['https://www.alpha-innotec.com/de/kontakt/beratung-und-vertrieb/fachpartnersuche']

    def parse(self, response: Response, **kwargs):

        json_data = re.search(r'(\{"apiKey".+?)\);</script>', response.text).group(1)
        json_selector = Selector(text=json_data)
        for result in json_selector.jmespath('companies[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.alpha-innotec.com/de/kontakt/beratung-und-vertrieb/fachpartnersuche')

            item_loader.add_jmes('Name1', 'name')

            item_loader.add_jmes('Address', 'street')
            item_loader.add_jmes('City', 'city')
            item_loader.add_jmes('Zip', 'zipCode')
            item_loader.add_jmes('Email', 'email')
            item_loader.add_jmes('Website', 'web')
            item_loader.add_jmes('Phone', 'phone')
            item_loader.add_jmes('Latitude', 'lat')
            item_loader.add_jmes('Longitude', 'lng')

            parsed_result = item_loader.load_item()
            yield parsed_result
