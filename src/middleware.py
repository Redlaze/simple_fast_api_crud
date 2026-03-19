import time
import logging

from typing import (
    Callable,
)

from fastapi import (
    Request,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)


async def request_middleware(request: Request, call_next: Callable):
    request_id = id(request)
    start_time = time.perf_counter()
    logger.info(f'-> [{request_id}] {request.method} {request.url.path}')


    try:
        response = await call_next(request)
    except Exception as err:
        logger.error(f'<- [{request_id}] Error: {str(err)}')
        raise

    process_time = time.perf_counter() - start_time
    logger.info(
        f'<- [{request_id}] {request.method} {request.url.path} '
        f'[{response.status_code}] {process_time:.3f}s'
    )
    response.headers['X-Process-Time'] = str(process_time)

    return response
