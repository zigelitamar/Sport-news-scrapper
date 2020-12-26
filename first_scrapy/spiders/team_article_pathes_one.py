import scrapy
import consts


class OneArticlePathes(scrapy.Spider):
    """Scrapy spider class to fetch one articles addresses
    """
    name = "OneArticlePathes"

    def __init__(self, category=None, *args, **kwargs):
        super(OneArticlePathes, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.get('start_urls', '').split(', ')

    def parse(self, response):
        """Fetch all teams article addresses

        Args:
            response (dict): Dictionary that contains for each article: team name, article address, article image.
        """
        yield{
            'team': consts.TEAMS_ONE_REVERSE[response.url],
            'articles': (response.css("div.leagues-right-column a.article-top::attr(href)").getall() + response.css("div.leagues-right-column a.article-plain::attr(href)").getall())[:consts.MAX_ARTICLES_FROM_SITE],
            'images': (response.css('div.leagues-right-column img::attr(src)').getall())[:consts.MAX_ARTICLES_FROM_SITE]
        }
