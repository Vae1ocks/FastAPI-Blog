from setup.di_containers.main import MainContainer


def setup_container(modules: list) -> MainContainer:
    container = MainContainer()
    container.init_resources()
    container.wire(packages=modules)
    return container