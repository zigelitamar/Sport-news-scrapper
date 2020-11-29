import scrapy

PREFIX = 'https://www.one.co.il'

class ArticlePathes(scrapy.Spider):
    name = "ArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(ArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = [kwargs.get('start_urls', '')]

    def parse(self, response):
        yield{
            'main_article_path': response.css("div.leagues-right-column a.article-top::attr(href)").getall(),
            'article_paths': response.css("div.leagues-right-column a.article-plain::attr(href)").getall()
        }
