import scrapy

class Article(scrapy.Spider):
    name = "Article"

    def __init__(self, category=None, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'title': response.css("h1.article-main-title::text").get(),
            'sub_title': response.css("h2.article-sub-title::text").get(),
            'article_image': response.css("div.article-image img::attr(src)").getall(),
            'body': response.css("div.article-body-container p::text").getall(),
            'published_date': response.css("div.article-credit::text").get()
        }
