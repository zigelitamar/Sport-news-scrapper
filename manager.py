from one_handler import OneHandler
from walla_handler import WallaHandler
from sport5_handler import Sport5Handler

from Article import ArticleModel

class ArticlesManager(object):
    def __init__(self, teams: list):
        self.one_handler = OneHandler()
        self.walla_handler = WallaHandler()
        self.sport5_handler = Sport5Handler()

    def add_team(self, teams):
        print(f'Add {teams} to site scrapping')
        for team in teams:
            self.one_handler.add_team_page(team)
            self.walla_handler.add_team_page(team)
            self.sport5_handler.add_team_page(team)

        print(f'Succesfully added teams to site scrapping')
        return True
    
    def remove_team(self, teams):
        print(f'Remove {teams} to site scrapping')
        for team in teams:
            self.one_handler.remove_team_page(team)
            self.walla_handler.remove_team_page(team)
            self.sport5_handler.remove_team_page(team)

        print(f'Succesfully removed teams to site scrapping')
        return True

    def get_new_articles(self, one_teams_pages, walla_teams_pages, sport5_teams_pages):
        one_articles_list = self.one_handler.get_new_articles(one_teams_pages)
        walla_articles_list = self.walla_handler.get_new_articles(walla_teams_pages)
        sport5_articles_list = self.sport5_handler.get_new_articles(sport5_teams_pages)

        # all_articles = one_articles_list + walla_articles_list + sport5_articles_list
        

        return{
            'One': [article.json() for article in one_articles_list],
            'Walls': [article.json() for article in walla_articles_list],
            'Sport5': [article.json() for article in sport5_articles_list]
        }
    