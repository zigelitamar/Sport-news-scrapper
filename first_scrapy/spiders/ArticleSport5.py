import scrapy

class ArticleSport5(scrapy.Spider):
    name = "ArticleSport5"

    def __init__(self, category=None, *args, **kwargs):
        super(ArticleSport5, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        yield{
            'url': response.url,
            'title': response.css("h1.article-main::text").get(),
            'sub_title': response.css("h2.article-sub-main::text").get(),
            # 'article_image': response.css("header.entry-header img::attr(data-lazy)").get(),
            'body': '\n\n'.join(response.css("div.article-content p::text").getall()),
            'published_date': response.css("span.hint::text").get(),
            'source': 'Sport5'
        }
