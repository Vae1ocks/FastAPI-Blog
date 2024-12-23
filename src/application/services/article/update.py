from dataclasses import dataclass

import logging

from application.commiter import Commiter
from application.dto.article.article_update import ArticleUpdateDTO
from domain.entities.article.models import Article
from domain.entities.common.value_objects import BaseValueObject
from domain.repositories.article_repository import ArticleRepository

logger = logging.getLogger(__name__)


@dataclass
class ArticleUpdateService:
    article_repository: ArticleRepository
    commiter: Commiter

    async def __call__(self, dto: ArticleUpdateDTO) -> Article:
        article: Article = await self.article_repository.get_by_id(dto.id)
        for slot in dto.__slots__:  # noqa
            if slot == "id":
                continue
            attr = getattr(dto, slot)
            if attr is None:
                continue
            elif isinstance(attr, BaseValueObject):
                if attr.value is None:
                    continue

            setattr(article, slot, attr)
        self.article_repository.add(article)
        return article
