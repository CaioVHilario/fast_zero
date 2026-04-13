from http import HTTPStatus


def test_root_deve_retornar_links_documentation(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'API de estudos do curso de FastAPI para gerenciamento de /'
        'tarefas',
    }


# Teste do exercicio da aula 2
def test_deve_retornar_ok_e_html_escrito_ola_mundo__exercicio2(client):
    response = client.get('/exercicio2/')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá mundo! </h1>' in response.text
