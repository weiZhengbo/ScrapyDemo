# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-


import json

class DoubanMoviePipeline(object):
    def __init__(self):
        self.file = open('douban_new_movie.json', mode='w', encoding='UTF-8')

    def process_item(self, item, spider):
        line = 'the new movie list:'+'\n'

        for i in range(len(item['movie_star'])):
            movie_name={'movie_name':str(item['movie_name'][i]).replace(' ','')}
            movie_star = {'movie_star':str(item['movie_star'][i])}
            movie_url = {'movie_url': str(item['movie_url'][i])}
            line = line+json.dumps(movie_name,ensure_ascii=False)
            line = line + json.dumps(movie_star, ensure_ascii=False)
            line = line + json.dumps(movie_url, ensure_ascii=False)+'\n'
            self.file.write(line)
            print(line)
        return item

    def close_spider(self, spider):
        self.file.close()