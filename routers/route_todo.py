from fastapi import APIRouter, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from schemas import Todo, TodoBody
from database import db_create_todo
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)

    # デフォだと200番を返してしまう。Postの返り値には201にしたいのでカスタマイズ
    response.status_code = HTTP_201_CREATED

    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Create task failed"
    )
