# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb


class BolePipeline(object):
    def process_item(self, item, spider):
        return item


#调用scrapy的ImagesPipeline方法获取图片路径并保存
class SaveImagePath(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_path = value['path']
        item['cover_image_path'] = image_path
        return item


#调用scrapy的JsonItemExporter方法将数据保存为json文件
class SavaJsonExporter(object):
    def __init__(self):
        self.file = open('data.json','wb')
        self.exproter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exproter.start_exporting()

    def close_spider(self,spider):
        self.exproter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exproter.export_item(item)
        return item


#连接mysql并保存数据
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','root','root','bole',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert = """
            insert into boledata(title,url,datetime,comment_nums,fab_nums,fav_nums,tags,url_id,cover_image,category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert,(item['title'],item['url'],item['datetime'],item['comment_nums'],item['fab_nums'],item['fav_nums'],item['tags'],item['url_id'],item['cover_image'],item['category']))
        self.conn.commit()