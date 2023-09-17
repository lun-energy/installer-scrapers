import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)


def main():
    # generate_input('data_backup\\Borrower Name Schedule.xlsx')

    settings = get_project_settings()

    process = CrawlerProcess(settings, install_root_handler=False)

    # logging
    configure_logging()
    # process.crawl(spider)
    process.start(install_signal_handlers=True)
    logger.info('Scraping Completed!')

if __name__ == '__main__':
    main()
