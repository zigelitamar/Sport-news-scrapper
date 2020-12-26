import scrapy
from datetime import datetime

class ArticleOne(scrapy.Spider):
    """Scrapy spider class to fetch sport5 articles
    """
    name = "ArticleOne"

    def __init__(self, category=None, *args, **kwargs):
        super(ArticleOne, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        """Main method of Scrapy spiders. return full article details

        Args:
            response (dict): Article details
        """
        yield{
            'url': response.url,
            'title': response.css("h1.article-main-title::text").get(),
            'sub_title': response.css("h2.article-sub-title::text").get(),
            'article_image': (response.css("div.article-image img::attr(src)").get()),
            'body': '\n\n'.join(response.css("div.article-body-container p::text").getall()),
            'published_date': (response.css("div.article-credit::text").get().replace('|','').replace('\r',''))[1:],
            'source': 'One'
        }
