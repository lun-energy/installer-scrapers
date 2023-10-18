from urllib.parse import urlencode

from haversine import inverse_haversine, Direction
from scrapy import Request

from StoreScraper.spiders import VaillantSpider


class VaillantDkSpider(VaillantSpider):
    name = "vaillant.dk"
    country = 'DK'

    def start_requests(self):
        radius = 50
        for coord in self.calculate_coordinates(radius=radius):
            sw = inverse_haversine(coord, distance=radius, direction=Direction.SOUTHWEST)
            ne = inverse_haversine(coord, distance=radius, direction=Direction.NORTHEAST)
            params = {
                'qualifications': 'varmepumper+%28salg%29',
                'c': self.point_to_string(coord),
                'sw': self.point_to_string(sw),
                'ne': self.point_to_string(ne),

            }
            yield Request(url='https://www.vaillant.dk/kunder/rad/forhandler/?' + urlencode(params))

    def calculate_coordinates(self, **kwargs):
        return super().calculate_coordinates(radius=kwargs.get('radius'), ne_coordinates=(57.96, 15.56), sw_coordinates=(54.46, 7.72))
