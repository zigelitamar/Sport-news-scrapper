import os
import scrapy
import json
import subprocess

from flask import Flask
from flask_restful import Api
from flask import jsonify
from first_scrapy.models.Article import Article

PREFIX = 'https://www.one.co.il'

app = Flask(__name__)

@app.route('/article/<path:start_urls>')
def article(start_urls):
    articles = []
    if os.path.exists("./out.json"):
        os.remove("./out.json")
    
    # start_urls = ' '.join(start_urls)
    
    
    subprocess.run(['scrapy', 'crawl', 'Article', "-a", f"start_urls={start_urls}", '-o', 'out.json'])
    with open('out.json') as json_file:
        data = json.load(json_file)
        for article in data:
            article_object = Article(**article)
            articles.append(article_object.as_json())

        return jsonify(articles)

@app.route('/articlespaths')
def articles_paths():
    addresses = []
    if os.path.exists("./out.json"):
        os.remove("./out.json")
    
    start_urls = 'https://www.one.co.il/Soccer/team/3'
    
    
    subprocess.run(['scrapy', 'crawl', 'ArticlePathes', "-a", f"start_urls={start_urls}", '-o', 'out.json'])
    with open('out.json') as json_file:
        data = json.load(json_file)
        for addresses in data:
            for key in addresses.keys():
                addresses[key] = [PREFIX + add for add in addresses[key]]

    return {'address': addresses}
    
if __name__ == '__main__':
    app.run(debug=True)