from fastapi import (
    APIRouter,
)
from sqlalchemy import select, delete

from src.database import (
    Base,
    engine,
    SessionDep,
)
from .models import (
    BookModel,
)
from .schemas import (
    BookAddSchema,
    PaginationDep,
)


books_router = APIRouter(
    prefix='/books',
    tags=['books'],
)


@books_router.get('/refresh_database', description='Сбрасывает БД')
async def refresh_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return {'status': 200}


@books_router.post('/', description='Добавляет книги')
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()

    return {'status': 200}


@books_router.get('/all', description='Получает все книги')
async def get_all_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)

    return result.scalars().all()


@books_router.delete('/', description='Удаляет книгу по фильтрам')
async def delete_books(data: BookAddSchema, session: SessionDep):
    stmt = delete(BookModel).where(
        BookModel.title == data.title,
        BookModel.author == data.author,
    )

    result = await session.execute(stmt)
    await session.commit()

    return {'count': result.rowcount}


@books_router.get('/', description='Получает список книг с учетом пагинации')
async def get_books(session: SessionDep, pagination: PaginationDep):
    query = select(
        BookModel,
    ).limit(
        pagination.limit,
    ).offset(
        pagination.offset,
    )
    result = await session.execute(query)

    return result.scalars().all()
