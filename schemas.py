# エンドポイントに渡すデータの型とかレスポンスのデータの型を定義していく。
from pydantic import BaseModel


class Todo(BaseModel):
    id: str
    title: str
    description: str


class TodoBody(BaseModel):
    title: str
    description: str
