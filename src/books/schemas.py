from typing import (
    Annotated,
)

from fastapi.params import Depends
from pydantic import (
    BaseModel,
    Field,
)


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BaseModel):
    id: int
    title: str
    author: str


class PaginationParams(BaseModel):
    limit: int = Field(
        default=5,
        ge=0,
        le=100,
        description='Кол-во элементов на странице',
    )
    offset: int = Field(
        default=0,
        ge=0,
        description='Смещение для пагинации',
    )


PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]
