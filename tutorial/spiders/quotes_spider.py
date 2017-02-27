# -*- coding: utf-8 -*-
import scrapy
import req
import json
from tutorial.items import TutorialItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

class LaGou(scrapy.Spider):
    name = 'lagou'

    start_urls = (
        'https://www.lagou.com/zhaopin/',
    )
    TotalPageCount = 0
    CurPage = 1
    cur = 0
    myurl = 'http://www.lagou.com/jobs/positionAjax.json?px=new&city='
    city = u'深圳'
    kds = [u'大数据',u'爬虫','python']
    kd = kds[0]

    def start_requests(self):
        return [scrapy.http.FormRequest(self.myurl,formdata={'pn':str(self.CurPage),'kd':self.kd},                                              callback=self.parse)]

    def parse(self, response):
        print(response.body)
        with open('lagou.html','wb') as f:
            f.write(response.body)
        item = TutorialItem
        jdict = json.loads(response.body)
        jcontent = jdict['content']
        jposresult = jcontent['PositionResult']
        jresult = jposresult['result']
        self.TotalPageCount = jposresult['TotalCount'] /15 + 1

        for each in jresult:
            item['City'] = each['city']
            item['BusinessZones'] = each['businessZones']
            item['CompanyName'] = each['companyName']
            item['CompanySize'] = each['companySize']
            item['FinanceStage'] = each['financeStage']
            item['PositionName'] = each['positionName']
            item['WorkYear'] = each['workYear']
            sal = each['salary']
            sal = sal.split('-')

            if len(sal) == 1:
                item['SalaryMax'] = int(sal[0][:sal[0].find('k')])
            else:
                item['SalaryMax'] = int(sal[1][:sal[1].find('k')])
            item['SalaryMin'] = int(sal[0][:sal[0].find('k')])
            item['SalaryAvg'] = (item['salaryMin'] + item['salaryMax'])/2
            item['KeyWord'] = self.kd
            yield item

        if self.CurPage <= self.TotalPageCount:
            self.CurPage += 1
            yield scrapy.http.FormRequest(self.myurl,formdata={'pn':str(self.CurPage),'kd':self.kd},
                                          callback=self.parse)
        elif self.cur < len(self.kds) - 1:
            self.CurPage = 1
            self.TotalPageCount = 0
            self.cur += 1
            self.kd = self.kds[self.cur]
            yield scrapy.http.FormRequest(self.myurl,formdata={'pn':str(self.CurPage),'kd':self.kd},
                                          callback=self.parse)

        a =response.body
        print(a.decode())
