# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class DoubanMovieCrawspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('douban_movie.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = 'the list:' + '\n'
        for i in range(len(item['name'])):
            name = {"name": item['name'][i]}
            year = {"year": item['year'][i]}
            score = {"score": item['score'][i]}
            director = {"director": item['director'][i]}
            classification = {"classification": item['classification'][i]}
            try:
                actor = {"actor": item['actor'][i]}
            except:
                actor = {"actor": "无"}

            line = line + json.dumps(name, ensure_ascii=False)
            line = line + json.dumps(year, ensure_ascii=False)
            line = line + json.dumps(score, ensure_ascii=False)
            line = line + json.dumps(director, ensure_ascii=False)
            line = line + json.dumps(classification, ensure_ascii=False)
            line = line + json.dumps(actor, ensure_ascii=False) + "\n"

        self.file.write(line)

    def close_spider(self, spider):
        self.file.close()