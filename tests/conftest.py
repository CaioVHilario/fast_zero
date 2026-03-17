from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import Settings, get_password_hash


# fixture para fazer o arrange dos testes abrindo o cliente de teste
@pytest.fixture
def client(session):
    def get_session_override():
        # Função para chamar a fixture session que usa a banco de dados em
        # memória, para testes unitários.
        return session

    with TestClient(app) as client:
        # Sobreescreve a get_session quando o endpoint POST for chamado
        #  e retorna a fixture session para não "sujar" o banco de dados
        # de produção, usando apenas a memoria
        app.dependency_overrides[get_session] = get_session_override
        yield client

    # Limpa o que foi sobreescrito
    app.dependency_overrides.clear()


# fixture para configurar e limpar o banco de dados para cada teste, isolando
# os testes para que um teste não interfira no outro
@pytest.fixture
def session():
    # cria o banco de dados em memoria apenas para testes unitários
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # pega todos os metadados das tabelas já registradas e cria eles
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

    # função para alterar o método created_at, updated_at do objeto target
    def fake_time_hook(mapper, connection, target):
        # condição para ver se target (User) tem 'created_at'
        if hasattr(target, 'created_at'):
            target.created_at = time
        # condição para ver se target (User) tem 'updated_at'
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    # quando o evento acontecer escuta antes e chama fake_time_hook
    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    # apos o evento acontecer remove
    event.remove(model, 'before_insert', fake_time_hook)


# fixture apenas para retornar _mock_db_time
@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    password = 'testtest'
    user = User(
        username='Teste',
        password=get_password_hash(password),
        email='teste@test.com',
    )

    user.clean_password = password

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(client, user):

    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
