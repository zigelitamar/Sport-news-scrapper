class Article(object):
    def __init__(self, title, sub_title, body, article_image, published_date):
        self.title = title
        self.sub_title = sub_title
        self.body = body
        self.article_image = article_image
        self.published_date = published_date

    def as_json(self):
        return vars(self)