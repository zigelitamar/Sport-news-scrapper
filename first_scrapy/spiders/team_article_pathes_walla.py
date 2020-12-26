import scrapy
import consts

class WallaArticlePathes(scrapy.Spider):
    """Scrapy spider class to fetch walla articles addresses
    """
    name = "WallaArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(WallaArticlePathes, self).__init__(*args, **kwargs)

        
        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        """Fetch all teams article addresses

        Args:
            response (dict): Dictionary that contains for each article: team name, article address, article image.
        """
        yield{
            'team': consts.TEAMS_WALLA_REVERSE[response.url],
            'articles': (response.css("section.sequence.common-articles a::attr(href)").getall())[:consts.MAX_ARTICLES_FROM_SITE],
            'images': (response.css("article.article.fc.common-article img::attr(src)").getall())[:consts.MAX_ARTICLES_FROM_SITE]
        }
