from typing import (
    Callable,
)

import uvicorn
from fastapi import (
    FastAPI,
    Request,
)

from src.books.router import (
    books_router,
)
from src.middleware import (
    request_middleware,
)


app = FastAPI(title='API Example')
app.include_router(books_router)

@app.middleware('http')
async def log_requests(request: Request, call_next: Callable):
    return await request_middleware(request, call_next)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
