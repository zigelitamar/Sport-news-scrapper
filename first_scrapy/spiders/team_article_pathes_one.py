import scrapy
import consts


class OneArticlePathes(scrapy.Spider):
    name = "OneArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(OneArticlePathes, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.get('start_urls', '').split(', ')
        print('INT ONEEEEEEEEEEEEEEEE')

    def parse(self, response):
        yield{
            'team': consts.TEAMS_ONE_REVERSE[response.url],
            'articles': (response.css("div.leagues-right-column a.article-top::attr(href)").getall() + response.css("div.leagues-right-column a.article-plain::attr(href)").getall())[:consts.MAX_ARTICLES_FROM_SITE],
            'images': (response.css('div.leagues-right-column img::attr(src)').getall())[:consts.MAX_ARTICLES_FROM_SITE]
        }
