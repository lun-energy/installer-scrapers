from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class VeinstallatoerDkSpider(base_spider.BaseSpider):
    name = "veinstallatoer.dk"
    country = 'DK'

    start_urls = ['https://veinstallatoer.dk/find-installatoer/?post_code=&range=300&category=22']

    def parse(self, response: Response, **kwargs):
        for result in response.css('div.tile_holder'):
            item_loader = ItemLoader(item=StoreItem(), selector=result)

            item_loader.add_css('Name1', '.tile_company_name strong::text')
            item_loader.add_css('City', '.tile_company_address::text')

            item_loader.add_xpath('Email', './/a[contains(@href, "mailto:")]//text()')
            item_loader.add_xpath('Website', './/a[normalize-space(@class)="button tile_company_button full_width"]/@href')
            item_loader.add_xpath('Phone', './/a[contains(@href, "tel:")]//text()')

            item_loader.add_xpath('Latitude', '@data-lat')
            item_loader.add_xpath('Longitude', '@data-lng')

            parsed_result = item_loader.load_item()
            yield self.add_unique_address_id(parsed_result)
