from urllib.parse import urlparse, parse_qs, urlencode

from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class VdiSpider(base_spider.BaseSpider):
    name = "vdi-sachkundiger-waermepumpe.de"

    start_urls = [
        'https://www.vdi-sachkundiger-waermepumpe.de/index.php?type=180927&tx_bwpvdiwp_database%5Bcontroller%5D=Database&tx_bwpvdiwp_database%5Baction%5D=filter&tx_bwpvdiwp_database%5Bpage%5D=0&tx_bwpvdiwp_database%5Bdegree%5D=1&tx_bwpvdiwp_database%5Bname%5D=&tx_bwpvdiwp_database%5Bcompany%5D=&tx_bwpvdiwp_database%5Bplace%5D=',
        'https://www.vdi-sachkundiger-waermepumpe.de/index.php?type=180927&tx_bwpvdiwp_database%5Bcontroller%5D=Database&tx_bwpvdiwp_database%5Baction%5D=filter&tx_bwpvdiwp_database%5Bpage%5D=0&tx_bwpvdiwp_database%5Bdegree%5D=3&tx_bwpvdiwp_database%5Bname%5D=&tx_bwpvdiwp_database%5Bcompany%5D=&tx_bwpvdiwp_database%5Bplace%5D='
    ]

    def parse(self, response: Response, **kwargs):

        for result in response.xpath('//td[normalize-space(@class)="company"]'):

            item_loader = ItemLoader(item=StoreItem(), selector=result)
            item_loader.add_xpath('Name1', 'a/text()')

            address_parts = [n.xpath('text()').get(default='') for n in result.xpath('div[normalize-space(@class)="company-address"]/div')]
            street, postal_code, city = self.parse_address(','.join(address_parts))

            item_loader.add_value('Address', street)
            item_loader.add_value('Zip', postal_code)
            item_loader.add_value('City', city)
            parsed_item = item_loader.load_item()

            parsed_result = item_loader.load_item()
            yield self.add_unique_address_id(parsed_result)

        query_parameters = parse_qs(urlparse(response.url).query)
        current_page = int(query_parameters['tx_bwpvdiwp_database[page]'][0])
        last_page = int(response.xpath('//option/@value').getall()[-1])
        if current_page < last_page:
            query_parameters['tx_bwpvdiwp_database[page]'] = current_page + 1
            yield Request(url='https://www.vdi-sachkundiger-waermepumpe.de/index.php?' + urlencode(query_parameters, doseq=True))
