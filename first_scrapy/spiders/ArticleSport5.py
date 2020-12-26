import scrapy
from datetime import datetime


class ArticleSport5(scrapy.Spider):
    """Scrapy spider class to fetch sport5 articles
    """
    name = "ArticleSport5"

    def __init__(self, category=None, *args, **kwargs):
        super(ArticleSport5, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        """Main method of Scrapy spiders. return full article details

        Args:
            response (dict): Article details
        """
        yield{
            'url': response.url,
            'title': response.css("h1.article-main::text").get().replace('  ', '').replace('\n', '').replace('\r', ''),
            'sub_title': response.css("h2.article-sub-main::text").get().replace('  ', '').replace('\n', '').replace('\r', ''),
            'body': "\n\n".join([p.replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '') for p in response.css("div.article-content p ").getall()]),
            'published_date': response.css("span.hint::text").get()[2:].replace('  ', '').replace('\n', '').replace('\r', '').replace('.', '/').replace('20 ', '2020 ').replace('-', ''),
            'source': 'Sport5'
        }

