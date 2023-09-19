import logging
import math
import re
from abc import ABC

import haversine
import scrapy.core.scraper
import scrapy.utils
import scrapy.utils.misc


def warn_on_generator_with_return_value_stub(spider, callable):
    pass


scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub


class BaseSpider(scrapy.Spider, ABC):
    name = 'base_spider'

    DEFAULT_AJAX_REQUEST_HEADER = {
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.configure_logging_extended()

    @staticmethod
    def configure_logging_extended(logging_format: str = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'):
        modules = [
            # 'scrapy.statscollectors',
            'scrapy.crawler',
            'scrapy.utils.log',
            'scrapy.middleware',
            'scrapy.core.engine',
            'scrapy.core.scraper',
            'scrapy.addons',
            __name__
        ]
        for module in modules:
            logger = logging.getLogger(module)
            logger.setLevel(logging.WARNING)

        for handler in logging.root.handlers:
            handler.formatter = NoTracebackFormatter(logging_format)
            handler.addFilter(ContentFilter())

    @staticmethod
    def calculate_coordinates(radius: int = 100, unit: haversine.Unit = haversine.Unit.KILOMETERS):
        NW_COORDINATES = (55.1, 5.5)
        NE_COORDINATES = (55.1, 15.5)
        SW_COORDINATES = (47.2, 5.5)
        SE_COORDINATES = (47.2, 15.5)

        NW_NE_DISTANCE = math.ceil(haversine.haversine(NW_COORDINATES, NE_COORDINATES, unit=unit))
        NW_SW_DISTANCE = math.ceil(haversine.haversine(NW_COORDINATES, SW_COORDINATES, unit=unit))
        result_coordinates = []
        for h_distance in range(0, NW_SW_DISTANCE, radius):
            start_coordinates = haversine.inverse_haversine(NW_COORDINATES, h_distance, haversine.Direction.SOUTH)
            for w_distance in range(0, NW_NE_DISTANCE, radius):
                new_coordinates = haversine.inverse_haversine(start_coordinates, w_distance, haversine.Direction.EAST)
                result_coordinates.append(new_coordinates)
                # print(f'{new_coordinates[0]},{new_coordinates[1]},')

        return result_coordinates

    @staticmethod
    def parse_address(input_string: str) -> tuple[str, str, str]:
        address_parts = input_string.split(',')
        street = address_parts[0:-1][0]
        postal_code = re.search('\\d+', address_parts[-1]).group(0)
        city = address_parts[-1].replace(postal_code, '')
        return street.strip(), postal_code.strip(), city.strip()


class ContentFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'spider'):
            record.name = record.spider.name
        elif hasattr(record, 'crawler'):
            record.name = record.crawler.spidercls.name
        else:
            pass
        return True


class NoTracebackFormatter(logging.Formatter):
    def formatException(self, ei):
        # return ''
        pass

    def formatStack(self, stack_info):
        # return ''
        pass
