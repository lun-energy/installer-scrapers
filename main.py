import logging
import os
from os.path import exists

from colorama import Fore, Style, init
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from StoreScraper.spiders import PanasonicSpider, DaikinSpider, WeishauptSpider, BuderusSpider, WolfSpider, NibeSpider, BoschSpider, ViessmannSpider, VaillantSpider, AlphaInnotecSpider, WaermepumpeSpider, VdiSpider
from excel_exporter import excel_exporter

logger = logging.getLogger(__name__)


def main():
    init()

    # os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')

    settings = get_project_settings()

    data_file = settings.get('DATA_FILE')
    excel_file = settings.get('EXCEL_FILE')

    if exists(data_file):
        os.remove(data_file)

    if bool(settings.get('HTTPPROXY_ENABLED')):
        os.environ.setdefault('HTTP_PROXY', settings.get('HTTP_PROXY'))
        os.environ.setdefault('HTTPS_PROXY', settings.get('HTTP_PROXY'))

    process = CrawlerProcess(settings, install_root_handler=False)
    # logging
    configure_logging()

    process.crawl(DaikinSpider)
    process.crawl(WeishauptSpider)
    process.crawl(BuderusSpider)
    process.crawl(WolfSpider)
    process.crawl(NibeSpider)
    process.crawl(PanasonicSpider)
    process.crawl(BoschSpider)
    process.crawl(ViessmannSpider)
    process.crawl(VaillantSpider)
    process.crawl(AlphaInnotecSpider)
    process.crawl(WaermepumpeSpider)
    process.crawl(VdiSpider)

    process.start(install_signal_handlers=True)

    logger.info('SCRAPING COMPLETED.')
    logger.info('EXPORTING THE DATA TO EXCEL...')

    try:
        excel_exporter(data_file, excel_file)
        logging.info(f'{Fore.GREEN}{excel_file} was successfully saved.{Style.RESET_ALL}')
    except Exception as ex:
        logging.error(f'{Fore.RED}{ex}{Style.RESET_ALL}', exc_info=False, stack_info=False)
    finally:
        input('Press Enter to exit the program...')


if __name__ == '__main__':
    main()
