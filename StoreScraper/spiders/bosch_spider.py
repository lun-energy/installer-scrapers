from scrapy.http import Response, JsonRequest
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class BoschSpider(base_spider.BaseSpider):
    name = "bosch-homecomfort.com"

    def start_requests(self):
        headers = {
            'Accept-Language': 'de-DE,de;q=0.8',
            'DTP-Country': 'DE',
            'DTP-Brand': 'bosch',
        }
        for lat, lng in self.calculate_coordinates(radius=25):
            json_data = {
                'Technologies': ['AirWaterHeatPump'],
                'Services': [],
                'Radius': 1000,
                'Location': {
                    'Latitude': lat,
                    'Longitude': lng,
                },
                'Take': 1000
            }
            yield JsonRequest(url='https://thernovo-api-functions.azurewebsites.net/api/DealerSearch', method='POST', data=json_data, headers=headers)

    def parse(self, response: Response, **kwargs):
        for result in response.jmespath('[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.bosch-homecomfort.com/de/de/wohngebaeude/service-und-support/installateur-finden/dealersearch/')
            item_loader.add_jmes('Name1', 'CompanyName')
            item_loader.add_jmes('Address', 'Address.Street')
            item_loader.add_jmes('City', 'Address.City')
            item_loader.add_jmes('Zip', 'Address.PostalCode')
            item_loader.add_jmes('Email', 'Email')
            item_loader.add_jmes('Website', 'Web')
            item_loader.add_jmes('Phone', 'Phone')
            item_loader.add_jmes('Latitude', 'Address.Latitude')
            item_loader.add_jmes('Longitude', 'Address.Longitude')

            parsed_result = item_loader.load_item()
            yield parsed_result
