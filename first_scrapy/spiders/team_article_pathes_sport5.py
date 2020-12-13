import scrapy

class Sport5ArticlePathes(scrapy.Spider):
    name = "Sport5ArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(Sport5ArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'articles': [address for address in response.css('div.info-container a::attr(href)').getall() if 'articles' in address],
            'images': response.css('div.info-container img::attr(src)').getall()
        }
