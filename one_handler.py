import os
import json
from flask import jsonify

from consts import ONE_TEAMS_PAGES
from utils import scrape_to_file
from Article import ArticleModel

class OneHandler(object):
    def __init__(self):
        self.PREFIX = 'https://www.one.co.il'

    def get_new_articles(self, teams):
        article_addresses_dict = self.get_article_pages(teams)

        exists_in_db, new_articles_addresses = self.split_articles(article_addresses_dict)

        new_articles = self.get_full_articles(new_articles_addresses)
        return exists_in_db + new_articles
    
    def split_articles(self, article_addresses_dict):
        exists_in_db = ArticleModel.find_by_articles_url(article_addresses_dict.keys())
        exists_in_db_list = [article.url for article in exists_in_db]
        
        article_addresses_dict_new = {}

        for key,value in article_addresses_dict.items():
            if key not in exists_in_db_list:
                article_addresses_dict_new[key] = value
        
        return exists_in_db, article_addresses_dict_new

    def get_article_pages(self, teams_pages):
        team_address_str = ', '.join(teams_pages)

        scrape_to_file('OneArticlePathes', team_address_str, 'out.json')

        all_teams_article_dict = {}

        with open('out.json') as json_file:
            data = json.load(json_file)
            for team_article_address in data:
                addresses_with_prefix = [self.PREFIX + part_address for part_address in team_article_address['articles']]
                zip_iterator = zip(addresses_with_prefix, [image for image in team_article_address['images']])
                articles_images_dict = dict(zip_iterator)
                for article in team_article_address['articles']:
                    all_teams_article_dict.update(articles_images_dict)
        return all_teams_article_dict
    
    def get_full_articles(self, article_urls):
        if not article_urls:
            return []
        
        articles = []
        articles_address_str = ', '.join(article_urls)
        
        scrape_to_file('ArticleOne', articles_address_str, 'articles.json')

        with open('articles.json') as json_file:
            data = json.load(json_file)
            for article in data:
                article['article_image'] = article_urls[article['url']]
                article_object = ArticleModel(**article)
                articles.append(article_object)

            if articles:
                ArticleModel.save_to_db_bulk(articles)
            return articles
