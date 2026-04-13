import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='Minha API de estudos do curso de FastAPI.')

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {
        'message': 'API de estudos do curso de FastAPI para gerenciamento de /'
        'tarefas',
    }


# Exercício da aula 2, fazer um endpoint que retorne um Olá mundo em HTML e
# fazer o teste com o pytest
@app.get(
    '/exercicio2/', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
async def html_olamundo():
    return """
    <html>
        <head>
            <title>API de estudos do curso de FastAPI</title>
        </head>
        <body>
            <h1> Olá mundo! </h1>
        </body>
    </html>"""
