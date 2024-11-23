from .user import map_users_table
from .article import map_articles_table
from .comment import map_comments_table


def map_tables():
    map_users_table()
    map_articles_table()
    map_comments_table()
