import scrapy
from datetime import datetime
import csv

class StorySpider(scrapy.Spider):
    name = 'stories'

    def start_requests(self):
        briefs_meta = [
            'recent-stories|local',
            'recent-stories|crime',
            'recent-stories|regional'
        ]
        for section in briefs_meta:
            yield scrapy.FormRequest(url = 'https://www.aspentimes.com/wp-admin/admin-ajax.php', 
                                    formdata={
                                        'action': 'get_more_briefs',
                                        'briefs_pointer': '0',
                                        'briefs_meta': section,
                                        'briefs_template_type': '',
                                        'briefs_nonce': 'ce86aca487'
                                    },
                                    callback = self.parse)

        with open('new.csv', 'w', encoding='UTF-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(('Title', 'Image', 'Article Text', 'Date', 'Author', 'URL'))

    def parse(self, response):
        for link in response.xpath('//article[@class="result "]//h5/a/@href').getall():
            yield scrapy.Request(url = link, callback = self.parse_article)    

    def parse_article(self, response):
        article = (response.xpath('//article[@class="flex-fill"]/h1/text()').get(),
                    response.xpath('//div[@class="p402_premium"]//img/@src').getall(),
                    ''.join(response.xpath('//div[@class="p402_premium"]//p/text()').getall()),
                    datetime.strptime(response.xpath('//div[@id="article-meta"]//time[@class="relative-date"]/@datetime').get(), "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y"),
                    response.xpath('//div[@class="editor-name"]/h6/a/text()').get(),
                    response.xpath('//meta[@property="og:url"]/@content').get())
        with open('new.csv', 'a', encoding='UTF-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(article)

