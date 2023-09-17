from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class BuderusSpider(base_spider.BaseSpider):
    name = "buderus.de"

    start_urls = ['https://www.buderus.de/blueprint/servlet/rest/dealerSearch/SearchLocations/ByLocator/DE/3584?rad=10&geo=&format=json']

    def parse(self, response: Response, **kwargs):
        for result in response.jmespath('Locations[*]'):

            services = result.jmespath('Services[*]').getall()
            for service in services:
                if service['Name'].strip() == 'HEATPUMP':
                    break
            else:
                continue

            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_value('Source', 'https://www.buderus.de/de/services-tools/experten-in-ihrer-naehe/fachbetriebe-in-ihrer-naehe-21776')
            item_loader.add_jmes('Name1', 'LocationName')

            item_loader.add_jmes('Address', 'Address.Address1')
            item_loader.add_jmes('City', 'Address.City')
            item_loader.add_jmes('Zip', 'Address.PostalCode')
            item_loader.add_jmes('Latitude', 'Geo.Latitude')
            item_loader.add_jmes('Longitude', 'Geo.Longitude')

            for item in result.jmespath('Resources').getall():
                item_name = item['Name'].strip()
                item_value = item['Value']
                if item_name == 'Phone':
                    item_loader.add_value('Phone', item_value)
                if item_name == 'E-Mail':
                    item_loader.add_value('Email', item_value)
                if item_name == 'Shop URL':
                    item_loader.add_value('Website', item_value)

            parsed_result = item_loader.load_item()
            yield parsed_result
