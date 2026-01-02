from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


# Teste do exercicio da aula 2
def test_exercicio2_deve_retornar_ok_e_html_escrito_ola_mundo():
    client = TestClient(app)

    response = client.get('/exercicio2')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá mundo! </h1>' in response.text
