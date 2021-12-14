from typing import List
from auth_utils import AuthJwtCsrf
from fastapi import APIRouter, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_csrf_protect.core import CsrfProtect
from schemas import Todo, TodoBody, SuccessMsg
from database import db_create_todo, db_delete_todo, db_get_single_todo, db_get_todos, db_update_todo
from starlette.status import HTTP_201_CREATED
from auth_utils import AuthJwtCsrf


router = APIRouter()
auth = AuthJwtCsrf()


@router.post('/api/todo', response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    # アクセスがあった際にVerifyをして新しいtokenを生成
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers
    )
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)

    # デフォだと200番を返してしまう。Postの返り値には201にしたいのでカスタマイズ
    response.status_code = HTTP_201_CREATED
    # 新しいtokenを渡す
    response.set_cookie(
        key="access_token", value=f"Bearer {new_token}", httponly=True, samesite="none", secure=True
    )

    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Create task failed"
    )


@router.get("/api/todo", response_model=List[Todo])
async def get_todos():
    res = await db_get_todos()
    return res


@router.get("/api/todo/{id}", response_model=Todo)
async def get_todo(id: str):
    res = await db_get_single_todo(id)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail=f"Task of ID: {id} doesn't exist"
    )


@router.put("/api/todo/{id}", response_model=Todo)
async def update_todo(id: str, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_update_todo(id, todo)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail="Update task failed"
    )


@router.delete("/api/todo/{id}", response_model=SuccessMsg)
async def delete_todo(id: str):
    res = await db_delete_todo(id)
    if res:
        return {"message": "Successfully deleted"}
    raise HTTPException(
        status_code=404, detail="Delete task failed"
    )
