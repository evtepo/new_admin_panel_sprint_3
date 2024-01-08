import abc
import json
from contextlib import contextmanager
from typing import Any, Dict, Union

from etl_backoff import backoff
from redis import Redis
from settings import Settings, redis_dsn


@contextmanager
@backoff(exceptions=Settings.redis_exceptions)
def get_redis(redis_url: Redis):
    """Функция для подключения к Redis"""

    try:
        yield redis_url
    finally:
        redis_url.close()


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: Redis, key: str) -> None:
        self.key = key
        self.redis_adapter = self.get_adapter(redis_adapter)

    def get_adapter(self, adapter: Redis) -> Redis:
        """Проверка изначального состояния"""
        valid_check = adapter.get(self.key)
        if valid_check:
            json.loads(valid_check)

        return adapter

    def save_state(self, state: Dict[str, Any]) -> Dict[Union[str, Any], None]:
        """Сохранение состояния в Redis"""
        self.redis_adapter.set(self.key, json.dumps(state))

    def retrieve_state(self) -> Dict[str, Any]:
        """Получение состояния из Redis"""
        try:
            return json.loads(self.redis_adapter.get(self.key))
        except:
            return {}


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.state = {}

    def set_state(self, key: str, value: Any) -> None:
        """Установка состояния для определённого ключа."""
        self.state[key] = value
        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Dict[Union[str, Any], None]:
        """Получение состояния по определённому ключу."""
        return self.storage.retrieve_state().get(key)


def get_state():
    redis = Redis.from_url(redis_dsn)
    key = "pg_data"
    with get_redis(redis) as redis:
        state = State(RedisStorage(redis, key))

        return state
