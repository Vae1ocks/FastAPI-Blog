import dishka.plotter
import uvloop
from dishka import AsyncContainer

from setup.configs import AllConfigs
from setup.ioc.setup import get_providers, create_async_ioc_container


def make_async_plot_container(configs: AllConfigs) -> AsyncContainer:
    return create_async_ioc_container(providers=get_providers(), configs=configs)


def generate_dependency_graph(container: AsyncContainer):
    return dishka.plotter.render_d2(container)


async def main():
    configs = AllConfigs()
    container = make_async_plot_container(configs)
    print(generate_dependency_graph(container))
    await container.close()


if __name__ == "__main__":
    uvloop.run(main())
