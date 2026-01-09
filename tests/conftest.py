from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


# fixture para fazer o arrange dos testes abrindo o cliente de teste
@pytest.fixture
def client():
    return TestClient(app)


# fixture para configurar e limpar o banco de dados para cada teste, isolando
# os testes para que um teste não interfia no outro
@pytest.fixture
def session():
    # cria o banco de dados em memoria apenas para testes unitários
    engine = create_engine('sqlite:///:memory:')
    # cria todos os metadados das tabelas já registradas e cria eles
    table_registry.metadata.create_all(engine)

    # abre a sessão do db e código para interagir com o banco
    with Session(engine) as session:
        yield session

    # limpa o banco em memoria para os proximos testes
    table_registry.metadata.drop_all(engine)
    # fecha todas as sessões abertas associadas a engine
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 10)):

    # função para alterar o método created_at do objeto target
    def fake_time_hook(mapper, connection, target):
        # condição para ver se target (User) tem 'created_at'
        if hasattr(target, 'created_at'):
            target.created_at = time

    # quando o evento acontecer escuta antes e chama fake_time_hook
    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    # apos o evento acontecer remove
    event.remove(model, 'before_insert', fake_time_hook)


# fixture apenas para retornar _mock_db_time
@pytest.fixture
def mock_db_time():
    return _mock_db_time
