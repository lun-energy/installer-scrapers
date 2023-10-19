import re

from scrapy import FormRequest, Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader

from StoreScraper.items import StoreItem
from StoreScraper.spiders import base_spider


class SparenergiDkSpider(base_spider.BaseSpider):
    name = "sparenergi.dk"
    country = 'DK'

    def start_requests(self):
        yield self.get_post_data_request()

    def parse(self, response: Response, **kwargs):

        operation = ''
        form_id = ''
        data = ''
        for json_parts in response.jmespath('[*]'):
            command = json_parts.jmespath('command').get()
            if command == 'insert':
                data = json_parts.jmespath('data').get()

            elif command == 'settings':
                operation = json_parts.jmespath('settings.ajax.*.submit[]._triggering_element_name').get()
            elif command == 'update_build_id':
                form_id = json_parts.jmespath('new').get()

        if operation == 'show_more':
            yield self.get_post_data_request(form_id=form_id)
        else:
            for result in Selector(text=data).xpath('//tbody/tr'):
                item_loader = ItemLoader(item=StoreItem(), selector=result)

                item_loader.add_css('Name1', '.field--name-name::text')

                address = result.css('.field--name-address::text').get()
                if ',' not in address:
                    address = re.sub(r'(\d+) (\d+)', r'\1, \2', address)

                street, postal_code, city = self.parse_address(address)

                item_loader.add_value('Address', street)
                item_loader.add_value('Zip', postal_code)
                item_loader.add_value('City', city)

                item_loader.add_css('Phone', '.field--name-telephone::text')
                item_loader.add_xpath('Email', './/a[contains(@href, "mailto:")]/@href')

                parsed_result = item_loader.load_item()
                yield self.add_unique_address_id(parsed_result)

    def get_post_data_request(self, form_id: str = ''):
        post_data = {
            'address': '',
            'name': '',
            'energy_solutions[]': '177',
            'form_build_id': form_id,
            'form_id': 'sparenergi_energy_solutions_ve_certified_company_list',
            '_triggering_element_name': 'show_more',
            '_triggering_element_value': 'Indlæs flere',
            '_drupal_ajax': '1',
            'ajax_page_state[theme]': 'sparenergi',
            'ajax_page_state[theme_token]': '',
            'ajax_page_state[libraries]': 'classy/base,classy/messages,core/drupal.tableresponsive,core/internal.jquery.form,core/normalize,google_tag/gtag,google_tag/gtag.ajax,google_tag/gtm,lazy/lazy,paragraphs/drupal.paragraphs.unpublished,sitewide_alert/init,sparenergi/global-styling,sparenergi/header,sparenergi_address/address_finder,sparenergi_anchors/sparenergi_anchors,sparenergi_common/cookie-redirect,sparenergi_frontend/select,sparenergi_frontend/tom_select_remove,sparenergi_legal_monster/legal-monster,sparenergi_legal_monster/update-cookies-permissions,sparenergi_legal_monster/update-external-scripts,sparenergi_navigation/search_menu,sparenergi_navigation/service_menu,sparenergi_watson_assistant/chatbot,system/base'
        }
        return FormRequest(url='https://sparenergi.dk/privat/tid-til-skifte-varmetype/find-varmepumpeinstallatoer?ajax_form=1&_wrapper_format=html&_wrapper_format=drupal_ajax',
                           headers=self.DEFAULT_AJAX_REQUEST_HEADER,
                           formdata=post_data)
