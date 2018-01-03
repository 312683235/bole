# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


#将所有数据转换换成自有类型，获取的数据默认为list
class BoleTakeFirst(ItemLoader):
    default_output_processor = TakeFirst()


#文章时间处理函数
def date_transform(value):
    value = value.replace('\n','').replace('\r','').replace(' ','').replace('·','')
    return value


#点赞、评论、收藏处理函数
def nums_transform(value):
    mth = re.match(".*?(\d+).*",value)
    if mth:
        nums = int(mth.group(1))
    else:
        nums = 0
    return nums


#图片下载处理函数
def return_value(value):
    return value


class BoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    datetime = scrapy.Field(
        input_processor = MapCompose(date_transform)
    )
    category = scrapy.Field()
    fab_nums = scrapy.Field(
        input_processor = MapCompose(nums_transform)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(nums_transform)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(nums_transform)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        output_processor = Join(",")
    )
    url = scrapy.Field()
    url_id = scrapy.Field()
    cover_image = scrapy.Field(
        #用于图片下载
        #output_processor = MapCompose(return_value)
    )
    cover_image_path = scrapy.Field()
