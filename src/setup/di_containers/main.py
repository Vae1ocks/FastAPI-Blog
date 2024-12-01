from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container

from setup.di_containers.application import ApplicationContainer
from setup.di_containers.db import DbContainer
from setup.di_containers.infrastructure import InfrastructureContainer


class MainContainer(DeclarativeContainer):
    infrastructure_container = Container(
        InfrastructureContainer,
    )
    db_container = Container(
        DbContainer,
    )
    application_container = Container(
        ApplicationContainer,
        infrastructure_container=infrastructure_container,
        db_container=db_container,
    )
