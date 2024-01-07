import logging
import random
import time

from functools import wraps


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, exceptions=None):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 1
            while True:
                t = start_sleep_time * (factor**n)
                try:
                    time.sleep(
                        random.uniform(
                            0.1,
                            t if t < border_sleep_time else border_sleep_time
                        )
                    )
                    return func(*args, **kwargs)
                except exceptions:
                    logging.error(
                        f"An error occurred from this list: {exceptions}. \
                        The error is caused by the function: {func.__name__}"
                    )
                    n += 1
                    continue

        return inner

    return func_wrapper
