import scrapy

class WallaArticlePathes(scrapy.Spider):
    name = "WallaArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(WallaArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'articles': response.css("section.sequence.common-articles a::attr(href)").getall(),
            'images': response.css("article.article.fc.common-article img::attr(src)").getall()
        }
