# -*- coding: utf-8 -*-
import scrapy
from Mapp.items import MappItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名字
    name = 'douban_spider'
    # 允许的域名，不在此域名下的数据不抓取
    allowed_domains = ['movie.douban.com']
    # 入口URL，扔到调度器中处理
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            douban_item = MappItem()
            # 序号
            douban_item['serial'] = i_item.xpath(".//div[@class='item']//em//text()").extract_first()
            # 电影名称
            douban_item['movie_name'] = \
                i_item.xpath(".//div[@class='info']//div[@class='hd']//a//span[1]//text()").extract_first()
            # 电影介绍,多行处理，拼接字符串
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']//p[1]//text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['movie_text'] = content_s
            # 星级
            douban_item['star'] =  i_item.xpath(".//div[@class='info']//div[@class='bd']//div[@class='star']//span[@class='rating_num']//text()").extract_first()
            # 电影评论数
            douban_item['evaluate'] = i_item.xpath(".//div[@class='info']//div[@class='bd']//div[@class='star']//span[4]//text()").extract_first()
            # 电影描述
            douban_item['describe'] =  i_item.xpath(".//div[@class='info']//div[@class='bd']//p[@class='quote']//span[@class='inq']//text()").extract_first()
            # s将数据传回管道中处理
            yield douban_item
        # 解析自动翻页的xpath
        next_like = response.xpath("//div[@class='paginator']//span[@class='next']/link/@href").extract()
        if next_like:
            next_like = next_like[0]  # 判断是否返回链接，有链接就去数据
            yield scrapy.Request("https://movie.douban.com/top250"+next_like, callback=self.parse)