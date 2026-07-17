#  python -m backend.app.service_tools.time_counter
import asyncio
import functools
import logging
import time
from typing import Callable

from backend.app.config.logging_config import logging_setup


logging_setup()

logger = logging.getLogger(__name__)


def get_executing_time(func: Callable):
    """Декоратор расчета времени выполнения функции."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = await func(*args, **kwargs)
        end = time.perf_counter_ns()
        elapsed = (end - start) / 1_000_000
        logger.info('Время выполнения функции %s: %.6f ms',
                    func.__name__, elapsed)
        return result
    return wrapper


@get_executing_time
async def counter():
    # time.sleep(1)
    logger.info('func counter executed')

# print(counter.__name__)
# print(get_executing_time.__annotations__)


# counter = get_executing_time(counter)
# counter()
# # decorator = get_executing_time
# # decorator(counter)

if __name__ == '__main__':
    asyncio.run(counter())
