from sqlalchemy.ext.asyncio import AsyncSession

from old.src.auth.models import User
from .models import Article


async def create_article(user: User, session: AsyncSession, data: dict):
    article = Article(**data, author=user)
    session.add(article)
    await session.commit()
    return article
