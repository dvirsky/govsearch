# -*- coding: utf-8 -*-

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'govsearch (+http://hasadna.org.il)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scraper.pipelines.ResolutionPipeline': 300,
}

CONCURRENT_REQUESTS = 30
CONCURRENT_REQUESTS_PER_DOMAIN = 30

# RETRY_TIMES = 5

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True

# LOG_ENABLED = False
LOG_LEVEL = 'INFO'
