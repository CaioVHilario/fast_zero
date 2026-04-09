from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import Settings, get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}sm9ASDM9f#$')


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


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


# fixture para configurar e limpar o banco de dados para cada teste, isolando
# os testes para que um teste não interfira no outro
@pytest_asyncio.fixture
async def session(engine):
    # pega todos os metadados das tabelas já registradas e cria eles
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    # abre a sessão do db e código para interagir com o banco
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # limpa o banco em memoria para os proximos testes
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


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


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    user.clean_password = password

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def other_user(session: AsyncSession):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    user.clean_password = password

    session.add(user)
    await session.commit()
    await session.refresh(user)

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
