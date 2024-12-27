from dishka import Provider, provide, Scope

from application.commiter import Commiter
from application.services.article.create import ArticleCreateService
from application.services.article.delete import ArticleDeleteService
from application.services.article.read import ArticleReadService
from application.services.article.update import ArticleUpdateService
from application.services.comment.create import CommentCreateService
from application.services.comment.update import CommentUpdateService
from application.services.jwt.refresh import RefreshTokenService
from application.services.user.checker import UserCheckerService
from application.services.user.login import LoginUsernamePasswordService
from application.services.user.user_registration import UserRegistrationService
from application.use_cases.article.create import ArticleCreateUseCase
from application.use_cases.article.delete import ArticleDeleteUseCase
from application.use_cases.article.read import ArticleReadDetailUseCase, ArticleListUseCase
from application.use_cases.article.update import ArticleUpdateUseCase
from application.use_cases.comment.create import CommentCreateUseCase
from application.use_cases.comment.update import CommentUpdateUseCase
from application.use_cases.user.login import LoginUseCase, RefreshUseCase
from application.use_cases.user.registration import (
    RegistrationUseCase,
    RegistrationConfirmationUseCase,
)
from infrastructure.persistence.sqlalchemy.commiter import SqlaCommiter


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    user_registration_service = provide(
        source=UserRegistrationService,
    )
    user_registration_usecase = provide(
        source=RegistrationUseCase,
    )
    user_confirmation_usecase = provide(
        RegistrationConfirmationUseCase,
    )
    user_checker_service = provide(
        source=UserCheckerService,
    )
    login_service = provide(
        LoginUsernamePasswordService,
    )
    login_usecase = provide(
        LoginUseCase,
    )
    commiter = provide(
        source=SqlaCommiter,
        provides=Commiter,
    )
    refresh_service = provide(
        source=RefreshTokenService,
    )
    refresh_usecase = provide(
        source=RefreshUseCase,
    )
    article_service = provide(
        source=ArticleCreateService,
    )
    article_create_use_case = provide(
        source=ArticleCreateUseCase,
    )
    article_update_service = provide(
        source=ArticleUpdateService,
    )
    article_update_use_case = provide(
        source=ArticleUpdateUseCase,
    )
    article_delete_service = provide(
        source=ArticleDeleteService,
    )
    article_delete_usecase = provide(
        source=ArticleDeleteUseCase,
    )
    article_read_service = provide(
        source=ArticleReadService,
    )
    article_read_usecase = provide(
        source=ArticleReadDetailUseCase,
    )
    article_list_usecase = provide(
        source=ArticleListUseCase,
    )
    comment_create_service = provide(
        source=CommentCreateService,
    )
    comment_create_usecase = provide(
        source=CommentCreateUseCase,
    )

