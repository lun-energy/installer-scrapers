from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class WolfSpider(base_spider.BaseSpider):
    name = "wolf.eu"

    start_urls = ['https://www.wolf.eu/de-de/ajax/2/fhw-search/get-results?distanceRadiusInKm=100&lng=&lat=&selectedCategories=heatPump']

    def parse(self, response: Response, **kwargs):
        for result in response.jmespath('data.partners[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_jmes('Name1', 'name')

            item_loader.add_jmes('Address', 'address.address1')
            item_loader.add_jmes('City', 'address.city')
            item_loader.add_jmes('Zip', 'address.postcode')

            item_loader.add_jmes('Phone', 'address.phoneNumber')
            item_loader.add_jmes('Latitude', 'address.lat')
            item_loader.add_jmes('Longitude', 'address.lng')

            parsed_result = item_loader.load_item()
            yield self.add_unique_address_id(parsed_result)
