from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Exercício da aula 2, fazer um endpoint que retorne um Olá mundo em HTML e
# fazer o teste com o pytest
@app.get(
    '/exercicio2/', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def html_olamundo():
    return """
    <html>
        <head>
            <title> Olá mundo!</title>
        </head>
        <body>
            <h1> Olá mundo! </h1>
        </body>
    </html>"""


# -----------------------------------------------------------------------------
# CRUD


# CREATE
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


# READ
@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


# UPDATE
@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


# DELETE
@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
