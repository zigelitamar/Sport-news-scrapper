import scrapy
from utils import fix_date
from datetime import datetime

class ArticleSportsWalla(scrapy.Spider):
    name = "ArticleSportsWalla"

    def __init__(self, category=None, *args, **kwargs):
        super(ArticleSportsWalla, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'url': response.url,
            'title': response.css("section.item-main-content h1::text").get(),
            'sub_title': response.css("section.item-main-content p::text").get(),
            # 'article_image': response.css("figure img::attr(src)").getall(),
            'body': '\n\n'.join(response.css("section.article-content p::text").getall()),
            'published_date': fix_date(response.css("div.wrap time::attr(datetime)").get()),
            'source': 'Walla'
        }
