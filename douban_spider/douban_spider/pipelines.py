# -*- coding: utf-8 -*-


import json
import codecs

class DoubanSpiderPipeline(object):
	def __init__(self):
		self.file=codecs.open('douban_movie2.json',mode='wb',encoding='utf-8')
	def process_item(self, item, spider):

		line='the list:'+'\n'
		for i in range(len(item['movie_name'])):

			movie_name = {"movie_name": item['movie_name'][i]}
			star={"start": item['star'][i]}
			quote={"quote": item['quote'][i]}
			line=line+json.dumps(movie_name,ensure_ascii=False)
			line=line+json.dumps(star,ensure_ascii=False)
			line=line+json.dumps(quote,ensure_ascii=False)+"\n"

		self.file.write(line)

	def close_spider(self,spider):
		self.file.close()