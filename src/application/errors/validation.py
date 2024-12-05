from application.common.error import ApplicationError


class ObjectExistsError(ApplicationError):
    pass


class FileNotImageError(ApplicationError):
    pass