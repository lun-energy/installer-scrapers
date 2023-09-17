from scrapy import FormRequest
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class WeishauptSpider(base_spider.BaseSpider):
    name = "weishaupt.de"

    def start_requests(self):
        url = 'https://www.weishaupt.de/kontakt/fachbetriebsfinder?action=result&middleware=dmind%2Fweishaupt-map%2Fjson-middleware&cHash=1b540c9af0811b22048553d51cd289b7'
        form_data = {
            'lat': '51.1657',
            'lng': '10.4515',
            'radius': '1000',
            'types[]': 'FACHBETRIEB'
        }
        yield FormRequest(url=url, formdata=form_data, headers=self.DEFAULT_AJAX_REQUEST_HEADER)

    def parse(self, response: Response, **kwargs):
        for result in response.jmespath('companies[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.weishaupt.de/kontakt/fachbetriebsfinder')
            item_loader.add_jmes('Name1', 'name1')
            item_loader.add_jmes('Name2', 'name2')
            item_loader.add_jmes('Address', 'address')
            item_loader.add_jmes('City', 'city')
            item_loader.add_jmes('Zip', 'zip')
            item_loader.add_jmes('Email', 'email')
            item_loader.add_jmes('Website', 'url')
            item_loader.add_jmes('Phone', 'tel')
            item_loader.add_jmes('Latitude', 'lat')
            item_loader.add_jmes('Longitude', 'lng')

            parsed_result = item_loader.load_item()
            yield parsed_result
