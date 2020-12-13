import scrapy

class ArticleSport1(scrapy.Spider):
    name = "ArticleSport1"

    def __init__(self, category=None, *args, **kwargs):
        super(ArticleSport1, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'title': response.css("h1.entry-title::text").get(),
            'sub_title': response.css("h2.post-excerpt::text").get(),
            'article_image': response.css("header.entry-header img::attr(data-lazy)").get(),
            'body': response.css("div.entry-content p::text").getall(),
            'published_date': response.css("div.posted-on time::attr(datetime)").get()
        }
