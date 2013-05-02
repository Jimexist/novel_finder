# Scrapy settings for novelbot project

SPIDER_MODULES = ['novelbot.spiders']
NEWSPIDER_MODULE = 'novelbot.spiders'
DEFAULT_ITEM_CLASS = 'novelbot.items.Website'

ITEM_PIPELINES = ['novelbot.pipelines.SaveToDBPipeline']
DOWNLOAD_DELAY = 2
