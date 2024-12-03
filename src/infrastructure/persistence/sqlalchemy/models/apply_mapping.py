from .user import map_users_table
from .article import map_articles_table
from .comment import map_comments_table


_is_mapped = False


def map_tables():
    global _is_mapped

    if _is_mapped:
        return

    _is_mapped = True
    map_users_table()
    map_articles_table()
    map_comments_table()
