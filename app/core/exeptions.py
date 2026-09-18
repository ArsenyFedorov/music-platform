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