# エンドポイントに渡すデータの型とかレスポンスのデータの型を定義していく。
from pydantic import BaseModel
from starlette.types import Message


class Todo(BaseModel):
    id: str
    title: str
    description: str


class TodoBody(BaseModel):
    title: str
    description: str


class SuccessMsg(BaseModel):
    message: str
