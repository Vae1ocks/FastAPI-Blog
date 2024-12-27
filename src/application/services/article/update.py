from dataclasses import dataclass

import logging

from application.dto.article.article_update import ArticleUpdateDTO
from application.errors.common.not_found import DoesNotExist
from domain.entities.article.models import Article
from domain.entities.common.value_objects import BaseValueObject
from domain.repositories.article_repository import ArticleRepository

logger = logging.getLogger(__name__)


@dataclass
class ArticleUpdateService:
    article_repository: ArticleRepository

    async def __call__(self, dto: ArticleUpdateDTO) -> Article:
        article: Article | None = await self.article_repository.get_by_id(dto.id)
        if article is None:
            raise DoesNotExist(obj_name="Article", obj_id=dto.id)

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
