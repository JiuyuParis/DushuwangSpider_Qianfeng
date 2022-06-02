import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider

from ..items import DushuwangItem


class CategorySpider(RedisCrawlSpider):
    name = 'category'
    allowed_domains = ['dushu.com']
    # start_urls = ['http://dushu.com/']
    # 作为redis push的关键子参数
    redis_key = 'start_url'

    # 定义爬取规则
    rules = (
        # 读书网图书分类的每个板块
        Rule(LinkExtractor(allow=r'/book/[\d]+_[\d]+.html'), callback='parse_item', follow=True),
        # 每个导航的链接
        Rule(LinkExtractor(restrict_xpaths='//div[@id="tab1"]/div[@class="class-nav"]/a'), callback='parse_item',
             follow=True),
    )

    # 解析网页，获取数据
    def parse_item(self, response):
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        books = response.xpath('//div[@class="bookslist"]/ul/li/div')
        for book in books:
            item = DushuwangItem()
            # 书名
            name = book.xpath('./h3/a/text()').get()
            p = book.xpath('./p')
            # 作者
            author = p[0].xpath('./text()').get()
            # 图书简介
            info = p[1].xpath('./text()').get()
            imgUrl = book.xpath('./div/a/img/@src').get()  # 图片暂时拿不出来
            item['name'] = '《' + name + '》'
            item['author'] = author
            item['imgUrl'] = imgUrl
            item['info'] = info
            yield item

    # 新版本的scrapy框架已经丢弃了这个函数的功能，但是并没有完全移除，虽然函数已经移除，但是还是在某些地方用到了这个，出现矛盾。
    # 重写一下这个方法
    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True)