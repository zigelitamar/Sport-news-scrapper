import scrapy
import consts

class WallaArticlePathes(scrapy.Spider):
    name = "WallaArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(WallaArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'team': consts.TEAMS_WALLA_REVERSE[response.url],
            'articles': (response.css("section.sequence.common-articles a::attr(href)").getall())[:consts.MAX_ARTICLES_FROM_SITE],
            'images': (response.css("article.article.fc.common-article img::attr(src)").getall())[:consts.MAX_ARTICLES_FROM_SITE]
        }
