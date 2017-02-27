# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    City = scrapy.Field()
    BusinessZones = scrapy.Field()
    CompanyName = scrapy.Field()
    CompanySize = scrapy.Field()
    FinanceStage = scrapy.Field()
    PositionName = scrapy.Field()
    WorkYear = scrapy.Field()
    SalaryMax = scrapy.Field()
    SalaryMin = scrapy.Field()
    SalaryAvg = scrapy.Field()
    KeyWord = scrapy.Field()

