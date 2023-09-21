from scrapy import FormRequest
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class WaermepumpeSpider(base_spider.BaseSpider):
    name = "waermepumpe.de"

    def start_requests(self):
        post_data = {
            'tx_bwpfps_fachpartnersuche[__referrer][@extension]': 'BwpFps',
            'tx_bwpfps_fachpartnersuche[__referrer][@controller]': 'Fachpartnersuche',
            'tx_bwpfps_fachpartnersuche[__referrer][@action]': 'index',
            'tx_bwpfps_fachpartnersuche[__referrer][arguments]': 'YTowOnt9f9e899de90908965bc6619a6fbb490248383a4d4',
            'tx_bwpfps_fachpartnersuche[__referrer][@request]': '{"@extension":"BwpFps","@controller":"Fachpartnersuche","@action":"index"}682a925e8f880fc3a831bf2f6759314d2db7bf2a',
            'tx_bwpfps_fachpartnersuche[__trustedProperties]': '{"search":1,"select":1,"place":1,"fpsubmit":1}c7cb76e2f53e04aa6a3fc82bde06e47616a8bc33',
            'tx_bwpfps_fachpartnersuche[search]': '1',
            'tx_bwpfps_fachpartnersuche[select]': 'fp',
            'tx_bwpfps_fachpartnersuche[sector]': '4',
            'tx_bwpfps_fachpartnersuche[place]': '',
            'tx_bwpfps_fachpartnersuche[fpsubmit]': 'Suchen'
        }
        yield FormRequest(url='https://www.waermepumpe.de/fachpartnersuche/fachpartner/?no_cache=1&tx_bwpfps_fachpartnersuche%5Bcontroller%5D=Fachpartnersuche', formdata=post_data)

    def parse(self, response: Response, **kwargs):
        for result in response.xpath('//div[@resultname]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_xpath('Name1', '@resultname')
            item_loader.add_xpath('City', '@place')
            item_loader.add_xpath('Email', './/a[contains(@href, "mailto:")]/text()')
            item_loader.add_xpath('Website', './/p[contains(text(), "Website:")]/a/@href')
            item_loader.add_xpath('Phone', './/a[contains(@href, "tel:")]/@href')
            item_loader.add_xpath('Latitude', '@latitude')
            item_loader.add_xpath('Longitude', '@longitude')

            address = result.xpath('.//p[span[contains(text(), "Adresse:")]]/text()').get()
            street, postal_code, city = self.parse_address(address)

            item_loader.add_value('Address', street)
            item_loader.add_value('Zip', postal_code)

            parsed_result = item_loader.load_item()
            yield self.add_unique_address_id(parsed_result)
