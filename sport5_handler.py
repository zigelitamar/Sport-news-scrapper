import os
import json
from flask import jsonify

from consts import SPORT5_TEAMS_PAGES
from utils import scrape_to_file
from Article import ArticleModel
from TeamModel import TeamModel


class Sport5Handler(object):
    def get_new_articles(self, teams):
        """Fetch teams new articles, That not exists in DB already, and creates ArticleModels from tham.

        Args:
            teams (list): List of teams to fetch thier articles.

        Returns:
            [ArticleModels]: List of article models of the teams that was given as parameter.
        """
        article_addresses_dict = self.get_article_pages(teams)

        exists_in_db, new_articles_addresses = self.split_articles(
            article_addresses_dict)

        new_articles = self.get_full_articles(new_articles_addresses)
        return exists_in_db + new_articles

    def split_articles(self, article_addresses_dict):
        """Split Article from article_addresses_dict to already fetched articles, and new articles

        Args:
            article_addresses_dict (dict): all fetched articles urls.

        Returns:
            (dict, dict): Tuple of already exists articles and new articles urls
        """
        exists_in_db = ArticleModel.find_by_articles_url(
            article_addresses_dict.keys())
        exists_in_db_list = [article.url for article in exists_in_db]

        article_addresses_dict_new = {}

        for key, value in article_addresses_dict.items():
            if key not in exists_in_db_list:
                article_addresses_dict_new[key] = value

        return exists_in_db, article_addresses_dict_new

    def get_article_pages(self, teams_pages):
        """From teams website pages, scraping the images and article urls

        Args:
            teams_pages (list): the teams main pages in One website

        Returns:
            [dict]: Dictionary of article details (article url, image, source)
        """
        team_address_str = ', '.join(teams_pages)

        scrape_to_file('Sport5ArticlePathes', team_address_str, 'out.json')

        all_teams_article_dict = {}

        with open('out.json') as json_file:
            data = json.load(json_file)
            for team_article_address in data:
                zip_iterator = zip(list(dict.fromkeys(
                    team_article_address['articles'])), [{'image': image, 'team': {team_article_address["team"]}} for image in team_article_address['images']])
                articles_images_dict = dict(zip_iterator)
                for article in articles_images_dict.keys():
                    if all_teams_article_dict.get(article):
                        all_teams_article_dict[article]['team'] = all_teams_article_dict.get(
                            article)['team'] | articles_images_dict[article]['team']
                    else:
                        all_teams_article_dict[article] = articles_images_dict[article]
        return all_teams_article_dict

    def get_full_articles(self, article_urls):
        """Scraping full article details from the urls in article_urls.

        Args:
            article_urls (list): list of articles urls to scrape from the website

        Returns:
            [ArticleModel]: List of Article models.
        """
        print("*********************")
        print(article_urls)
        print(type(article_urls))
        print("*********************")
        if not article_urls:
            return []

        articles = []
        articles_teams_dictionary = {}
        articles_address_str = ', '.join(article_urls)

        scrape_to_file('ArticleSport5', articles_address_str, 'articles.json')

        with open('articles.json', encoding="utf-8", errors='ignore') as json_file:
            try:
                data = json.load(json_file)

            except:
                print("something went wrong with an article at sport5")
                return []

            for article in data:
                article['article_image'] = article_urls[article['url']].get(
                    'image')
                # article['team'] = ', '.join(list(article_urls[article['url']].get('team')))
                article['article_teams'] = []
                articles_teams_dictionary[article['url']] = list(
                    article_urls[article['url']].get('team'))
                article_object = ArticleModel(**article)
                articles.append(article_object)

            if articles:
                ArticleModel.save_to_db_bulk(articles)

            urls = [article.url for article in articles]

            print(urls)

            for url in urls:
                article_obj = ArticleModel.find_by_articles_url_one(url)
                article_obj.article_teams = TeamModel.find_by_teams_names(
                    articles_teams_dictionary[url])
                article_obj.save_to_db()

            return articles
