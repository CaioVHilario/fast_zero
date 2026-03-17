from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI(title='Minha API de estudos do curso de FastAPI.')

app.include_router(users.router)
app.include_router(auth.router)


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
