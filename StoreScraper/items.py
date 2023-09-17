# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field


def format_whitespaces(input_string: str) -> str:
    if not input_string:
        return ''
    return re.sub('\s+', ' ', input_string).strip()


class StoreItem(scrapy.Item):
    Source = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Name1 = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Name2 = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Address = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    City = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Zip = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Email = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Phone = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Website = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Latitude = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Longitude = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
