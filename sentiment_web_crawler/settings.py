# -*- coding: utf-8 -*-

# Scrapy settings for sentiment_web_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sentiment_web_crawler'

SPIDER_MODULES = ['sentiment_web_crawler.spiders']
NEWSPIDER_MODULE = 'sentiment_web_crawler.spiders'
