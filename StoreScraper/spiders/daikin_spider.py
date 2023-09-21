from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class DaikinSpider(base_spider.BaseSpider):
    name = "daikin.de"

    start_urls = [
        'https://www.daikin.de/de_de/privatkunden/fachbetrieb-kontaktieren/_jcr_content/root/wide-content-container/dealer-locator.spatial.query.json.query.spatial.json?language=de&rows=2000&offset=0&f.facet_services=heating-and-or-hot-water&f.facet_dealersearch=partner-search-for-private-customers&']

    handle_httpstatus_list = [404]

    def parse(self, response: Response, **kwargs):
        for result in response.jmespath('results[*]'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_jmes('Name1', 'title')
            item_loader.add_jmes('Address', 'street')
            item_loader.add_jmes('City', 'city')
            item_loader.add_jmes('Zip', 'zip')

            geocode = result.jmespath('geocode').get().split(',')
            item_loader.add_value('Latitude', geocode[0])
            item_loader.add_value('Longitude', geocode[1])

            parsed_result = item_loader.load_item()

            url = result.jmespath('url').get()
            yield response.follow(url=url, callback=self.parse_contact_details, cb_kwargs={'item': parsed_result})

    def parse_contact_details(self, response: Response, **kwargs):
        item_loader = ItemLoader(item=kwargs.get('item'), response=response)
        item_loader.add_xpath('Email', '//a[normalize-space(@aria-label)="E-Mail"]/span/text()')
        item_loader.add_xpath('Website', '//a[normalize-space(@aria-label)="Website"]/span/text()')
        item_loader.add_xpath('Phone', '//a[normalize-space(@aria-label)="Telefon"]/span/text()')

        parsed_result = item_loader.load_item()
        yield self.add_unique_address_id(parsed_result)
