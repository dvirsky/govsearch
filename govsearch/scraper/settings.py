# -*- coding: utf-8 -*-

BOT_NAME = 'govsearch'

SPIDER_MODULES = ['govsearch.spiders']
NEWSPIDER_MODULE = 'govsearch.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'govsearch (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'govsearch.pipelines.DecisionPipeline': 300,
}

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
