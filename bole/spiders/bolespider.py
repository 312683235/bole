# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from bole.items import BoleArticleItem,BoleTakeFirst
from bole.utils.commons import get_md5


class BolespiderSpider(scrapy.Spider):
    name = 'bolespider'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #获取所有文章的urls，,并回调parse_detail函数解析
        nodes = response.xpath('//div[@id="archive"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        for node in nodes:
            url = node.xpath("@href").extract_first('')
            cover_image = node.xpath("img/@src").extract_first('')
            yield Request(url=parse.urljoin(response.url,url),meta={'cover_image':parse.urljoin(response.url,cover_image)},callback=self.parse_detail)

        #获取下一页的文章列表urls,并回调parse函数解析
        next_urls = response.xpath('//a[@class="next page-numbers"]/@href').extract()
        for next_url in next_urls:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    def parse_detail(self,response):
        cover_image = response.meta['cover_image']
        artcile_item = BoleArticleItem()

        item_loder = BoleTakeFirst(item=BoleArticleItem(),response=response)
        item_loder.add_xpath("title","//div[@class='entry-header']/h1/text()")
        item_loder.add_xpath("datetime","//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loder.add_xpath("category","//a[@rel='category tag']/text()")
        item_loder.add_xpath("fab_nums","//div[@class='post-adds']/span[1]/h10/text()")
        item_loder.add_xpath("fav_nums","//div[@class='post-adds']/span[2]/text()")
        item_loder.add_xpath("comment_nums","//span[@class='btn-bluet-bigger href-style hide-on-480']/text()")
        item_loder.add_xpath("content","//div[@class='entry']/text()")
        item_loder.add_xpath("tags","//p[@class='entry-meta-hide-on-mobile']/a[@rel='category tag']/following-sibling::a/text()")
        item_loder.add_value("url",response.url)
        item_loder.add_value("url_id",get_md5(response.url))
        item_loder.add_value("cover_image",cover_image)

        artcile_item = item_loder.load_item()

        yield artcile_item






