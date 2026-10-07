class AppError(Exception):
    """Базовая ошибка приложения"""

    status_code: int = 400

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class EmailAlreadyExistsError(AppError):
    """Конфликт почт"""

    status_code = 409

class UsernameAlreadyExistsError(AppError):
    """Конфликт имён"""

    status_code = 409

class FollowerAlreadeExistsError(AppError):
    """Конфлитк подписчкиков"""

    status_code = 409

class InvalidCredentialsError(AppError):
    """Ошибка аунтефикации"""

    status_code = 401

class InvalidTokenError(AppError):
    """Недействительный JWT"""
    
    status_code = 401


class NotFoundError(AppError):
    """Нет данных"""

    status_code = 404

