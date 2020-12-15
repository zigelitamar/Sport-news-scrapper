import os
import json
from flask import jsonify

from consts import WALLA_TEAMS_PAGES
from utils import scrape_to_file
from Article import ArticleModel
from db import db


class WallaHandler(object):
    # def get_teams_pages(self, teams: list):
    #     return {team: WALLA_TEAMS_PAGES[team] for team in teams}

    def get_new_articles(self, teams):
        article_addresses_dict = self.get_article_pages(teams)

        exists_in_db, new_articles_addresses = self.split_articles(
            article_addresses_dict)

        new_articles = self.get_full_articles(new_articles_addresses)
        return exists_in_db + new_articles

    def split_articles(self, article_addresses_dict):
        exists_in_db = ArticleModel.find_by_articles_url(
            article_addresses_dict.keys())
        exists_in_db_list = [article.url for article in exists_in_db]

        article_addresses_dict_new = {}

        for key, value in article_addresses_dict.items():
            if key not in exists_in_db_list:
                article_addresses_dict_new[key] = value

        return exists_in_db, article_addresses_dict_new

    def get_article_pages(self, teams_pages):
        team_address_str = ', '.join(teams_pages)

        scrape_to_file('WallaArticlePathes', team_address_str, 'out.json')

        all_teams_article_dict = {}

        with open('out.json', encoding="utf-8", errors='ignore') as json_file:
            data = json.load(json_file)
            for team_article_address in data:
                zip_iterator = zip(team_article_address['articles'], [
                                   image[2:] for image in team_article_address['images']])
                articles_images_dict = dict(zip_iterator)
                for article in team_article_address['articles']:
                    all_teams_article_dict.update(articles_images_dict)
        return all_teams_article_dict

    def get_full_articles(self, article_urls):
        if not article_urls:
            return []

        articles = []
        articles_address_str = ', '.join(article_urls)

        scrape_to_file('ArticleSportsWalla',
                       articles_address_str, 'articles.json')

        with open('articles.json', encoding="utf-8", errors='ignore') as json_file:
            data = json.load(json_file)
            for article in data:
                article['article_image'] = article_urls[article['url']]
                article_object = ArticleModel(**article)
                articles.append(article_object)

            if articles:
                ArticleModel.save_to_db_bulk(articles)
            return articles
