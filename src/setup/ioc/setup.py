from typing import Iterable

from dishka import Provider, AsyncContainer, make_async_container

from setup.configs import AllConfigs
from setup.ioc.application import ApplicationProvider
from setup.ioc.db import DatabaseProvider
from setup.ioc.infrastructure import InfrastructureProvider, InfrastructureRequestContextProvider
from setup.ioc.settings import ConfigProvider


def get_providers() -> Iterable[Provider]:
    db = (DatabaseProvider(),)
    infrastructure = (InfrastructureProvider(), InfrastructureRequestContextProvider())
    application = (ApplicationProvider(),)

    return (
        *(ConfigProvider(),),
        *db,
        *infrastructure,
        *application,
    )


def create_async_ioc_container(
    providers: Iterable[Provider],
    configs: AllConfigs,
) -> AsyncContainer:
    return make_async_container(
        *providers,
        context={AllConfigs: configs},
    )
