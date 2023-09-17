import logging


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
