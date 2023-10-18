from scrapy import FormRequest, Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class BoschDkSpider(base_spider.BaseSpider):
    name = "bosch-homecomfort.com - dk"
    country = 'DK'

    def start_requests(self):
        post_data = {
            'geoSearchEnable': 'true',
            'latitude': '56.25250574758756',
            'longitude': '10.188904171875048',
            'radius': '500',
            'query': 'Danmark',
            'fullQuery': '',
            'zoom': '6',
            'units': 'BOSCH-FACELIFT_HEATPUMP'
        }

        yield FormRequest(url='https://www.bosch-homecomfort.com/dk/da/privat/service/find-en-bosch-climate-partner/find-installator/dealers.json',
                          headers=self.DEFAULT_AJAX_REQUEST_HEADER,
                          formdata=post_data,
                          callback=self.download_details)

    def download_details(self, response: Response, **kwargs):
        for result in response.jmespath('[*]'):
            dealer_id = result.jmespath('customerNo').get()
            lat = result.jmespath('latitude').get()
            lng = result.jmespath('longitude').get()
            yield Request(url=f'https://www.bosch-homecomfort.com/dk/da/privat/service/find-en-bosch-climate-partner/find-installator/dealerdetails/{dealer_id}/?ajax=true',
                          cb_kwargs={'lat': lat, 'lng': lng},
                          callback=self.parse)

    def parse(self, response: Response, **kwargs):
        item_loader = ItemLoader(item=StoreItem(), selector=response)

        item_loader.add_css('Name1', '.dealer-item__title::text')

        address = response.css('.dealer-item__street::text').get()
        postal_code_city = response.css('.dealer-item__city::text').get()
        street, postal_code, city = self.parse_address(f'{address},{postal_code_city}')

        item_loader.add_value('Address', street)
        item_loader.add_value('Zip', postal_code)
        item_loader.add_value('City', city)

        item_loader.add_value('Latitude', response.request.cb_kwargs['lat'])
        item_loader.add_value('Longitude', response.request.cb_kwargs['lng'])

        item_loader.add_xpath('Email', '//a[contains(@href, "mailto:")]/@href')
        item_loader.add_xpath('Website', '//a[normalize-space(@aria-label)="Til websted"]/@href')
        item_loader.add_xpath('Phone', '//a[contains(@href, "tel:")]/@href')

        parsed_result = item_loader.load_item()
        yield self.add_unique_address_id(parsed_result)
