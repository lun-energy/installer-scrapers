# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import phonenumbers
import scrapy
from email_validator import validate_email, EmailNotValidError
from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field
from url_normalize import url_normalize


def format_whitespaces(input_string: str) -> str:
    if not input_string:
        return ''
    return re.sub('\s+', ' ', input_string).strip()


def format_phone(input_string: str) -> str:
    formatted_string = re.sub('[^0-9()+-]', '', input_string)
    if not formatted_string:
        return ''
    try:
        parsed_phone = phonenumbers.parse(input_string, 'DE')
        formatted_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.RFC3966).replace('tel:', '')
        return formatted_number
    except:
        return ''


def format_email(input_string: str) -> str:
    if input_string:
        try:
            email_info = validate_email(input_string.replace(' ', ''), check_deliverability=False)
            return email_info.normalized.lower()
        except EmailNotValidError:
            pass
    return ''


def format_website(input_string: str) -> str:
    try:
        return url_normalize(input_string)
    except:
        return ''


class StoreItem(scrapy.Item):
    Source = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Name1 = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Name2 = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Address = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    City = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Zip = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Email = Field(input_processor=MapCompose(format_whitespaces, format_email), output_processor=TakeFirst())
    Phone = Field(input_processor=MapCompose(format_whitespaces, format_phone), output_processor=TakeFirst())
    Website = Field(input_processor=MapCompose(format_whitespaces, format_website), output_processor=TakeFirst())
    Latitude = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())
    Longitude = Field(input_processor=MapCompose(format_whitespaces), output_processor=TakeFirst())

    MapboxId = Field(output_processor=TakeFirst())
    MapboxAddress = Field(output_processor=TakeFirst())
    EmailDomain = Field(output_processor=TakeFirst())
    Gmbh = Field(output_processor=TakeFirst())
