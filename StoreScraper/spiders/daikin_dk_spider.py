from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class DaikinDkSpider(base_spider.BaseSpider):
    name = "daikin.dk"
    country = 'DK'

    start_urls = [
        'https://www.daikin.dk/content/internet/internet-dk/da_DK/din-daikin-forhandler.query.spatial.json?language=da&rows=2000&offset=0&f.facet_dealer-types=Air-to-water-heatpump&f.facet_page-type=dealer-detail&']

    def parse(self, response, **kwargs):
        for result in response.jmespath('results[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_jmes('Name1', 'title')
            item_loader.add_jmes('Address', 'street')
            item_loader.add_jmes('City', 'city')
            item_loader.add_jmes('Zip', 'zip')
            item_loader.add_jmes('Email', 'email')
            item_loader.add_jmes('Website', 'website')
            item_loader.add_jmes('Phone', 'phone')

            geocode = result.jmespath('geocode').get().split(',')
            item_loader.add_value('Latitude', geocode[0])
            item_loader.add_value('Longitude', geocode[1])

            parsed_result = item_loader.load_item()
            yield self.add_unique_address_id(parsed_result)
