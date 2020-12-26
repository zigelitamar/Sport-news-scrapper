import scrapy
import consts

class Sport5ArticlePathes(scrapy.Spider):
    """Scrapy spider class to fetch sport5 articles addresses
    """
    name = "Sport5ArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(Sport5ArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        """Fetch all teams article addresses

        Args:
            response (dict): Dictionary that contains for each article: team name, article address, article image.
        """
        yield{
            'team': consts.TEAMS_SPORT5_REVERSE[response.url],
            'articles': ([address for address in response.css('div.info-container a::attr(href)').getall() if 'articles' in address])[:consts.MAX_ARTICLES_FROM_SITE],
            'images': (response.css('div.info-container img::attr(src)').getall())[:consts.MAX_ARTICLES_FROM_SITE]
        }
