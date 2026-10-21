from unittest.mock import Mock
import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


