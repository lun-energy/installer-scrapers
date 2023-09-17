class CustomProxyMiddleware(object):
    @staticmethod
    def process_request(request, spider):
        proxy_enabled = bool(spider.settings.get('HTTPPROXY_ENABLED'))
        if proxy_enabled:
            request.meta['proxy'] = spider.settings.get('HTTP_PROXY')