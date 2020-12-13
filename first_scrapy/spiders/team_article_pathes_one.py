import scrapy

class OneArticlePathes(scrapy.Spider):
    name = "OneArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(OneArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')
        print('INT ONEEEEEEEEEEEEEEEE')

    def parse(self, response):
        yield{
            'articles': response.css("div.leagues-right-column a.article-top::attr(href)").getall() + response.css("div.leagues-right-column a.article-plain::attr(href)").getall(),
            'images': [image.replace('src=', '').replace('"', '') for image in response.css('div.leagues-right-column a.article-top').get().split(' ') if 'images.one' in image] + response.css('div.leagues-right-column img::attr(src)').getall()
        }