from StoreScraper.spiders import ViessmannSpider


class ViessmannDkSpider(ViessmannSpider):
    name = "viessmann.dk"
    country = 'DK'

    def start_requests(self):
        for request in super().start_requests():
            new_url = request.url.replace('de-DE', 'da-DK')
            yield request.replace(url=new_url)

    def calculate_coordinates(self, **kwargs):
        return super().calculate_coordinates(radius=25, ne_coordinates=(57.96, 15.56), sw_coordinates=(54.46, 7.72))
