import os
import json
from flask import jsonify

from consts import ONE_TEAMS_PAGES
from utils import scrape_to_file
from Article import ArticleModel
from TeamModel import TeamModel


class OneHandler(object):
    def __init__(self):
        self.PREFIX = 'https://www.one.co.il'

    def get_new_articles(self, teams):
        article_addresses_dict = self.get_article_pages(teams)

        exists_in_db, new_articles_addresses = self.split_articles(
            article_addresses_dict)

        new_articles = self.get_full_articles(new_articles_addresses)
        return exists_in_db + new_articles

    def get_article_pages(self, teams_pages):
        team_address_str = ', '.join(teams_pages)

        scrape_to_file('OneArticlePathes', team_address_str, 'out.json')

        all_teams_article_dict = {}

        with open('out.json') as json_file:
            data = json.load(json_file)
            for team_article_address in data:
                addresses_with_prefix = [
                    self.PREFIX + part_address for part_address in team_article_address['articles']]

                zip_iterator = zip(addresses_with_prefix, [
                                   {'image': image, 'team': {team_article_address["team"]}} for image in team_article_address['images']])
                articles_images_dict = dict(zip_iterator)

                # for article in team_article_address['articles']:
                #     all_teams_article_dict.update(articles_images_dict)
                for article in articles_images_dict.keys():
                    if all_teams_article_dict.get(article):
                        all_teams_article_dict[article]['team'] = all_teams_article_dict.get(
                            article)['team'] | articles_images_dict[article]['team']
                    else:
                        all_teams_article_dict[article] = articles_images_dict[article]
        return all_teams_article_dict

    def split_articles(self, article_addresses_dict):
        exists_in_db = ArticleModel.find_by_articles_url(
            article_addresses_dict.keys())
        exists_in_db_list = [article.url for article in exists_in_db]

        article_addresses_dict_new = {}

        for key, value in article_addresses_dict.items():
            if key not in exists_in_db_list:
                article_addresses_dict_new[key] = value

        return exists_in_db, article_addresses_dict_new

    def get_full_articles(self, article_urls):
        if not article_urls:
            return []

        articles = []
        articles_teams_dictionary = {}
        articles_address_str = ', '.join(article_urls)

        scrape_to_file('ArticleOne', articles_address_str, 'articles.json')

        with open('articles.json', encoding="utf-8", errors='ignore') as json_file:
            try:
                data = json.load(json_file)

            except:
                print("something went wrong with an article at One")
                return []

            for article in data:
                try:
                    article['article_image'] = article_urls[article['url']].get(
                        'image')
                    # article['teams'] = ', '.join(list(article_urls[article['url']].get('team')))
                    article['article_teams'] = []
                    articles_teams_dictionary[article['url']] = list(
                        article_urls[article['url']].get('team'))
                    article_object = ArticleModel(**article)
                    articles.append(article_object)
                except:
                    article['article_image'] = ''
                    article['team'] = ''

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
