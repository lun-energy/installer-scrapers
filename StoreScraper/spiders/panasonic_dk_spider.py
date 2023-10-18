from scrapy import FormRequest

from StoreScraper.spiders import PanasonicSpider


class PanasonicDkSpider(PanasonicSpider):
    name = "panasonicproclub.com - dk"
    country = 'DK'

    def start_requests(self):
        post_data = {
            'geo': '0',
            'lat': '',
            'lng': '',
            'address': '',
            'selected_list': '105',
            'distance': '200',
            'search': ''
        }
        yield FormRequest(url='https://www.panasonicproclub.com/ifinder/DK_da/home/', formdata=post_data)
