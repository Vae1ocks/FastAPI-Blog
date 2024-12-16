from dishka import Provider, provide, Scope

from setup.configs import AllConfigs


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_configs(self) -> AllConfigs:
        return AllConfigs()