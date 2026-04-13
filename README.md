# Fast Zero

> API REST para gerenciamento de tarefas — baseada no curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/) da Live de Python, ministrado por Eduardo Mendes.

![Status](https://img.shields.io/badge/status-finalizado-brightgreen)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-CC%20BY--NC--SA-lightgrey)

---

## Sobre o Projeto

Este projeto é uma API de gerenciamento de tarefas (TODO List) desenvolvida ao longo do curso **FastAPI do Zero**. O foco é construir uma API robusta seguindo as melhores práticas do mercado, com autenticação JWT, banco de dados relacional, testes automatizados e deploy em produção.

**API em produção:** `https://todolist-fastzero.fly.dev/`

---

## O que você vai aprender

- Estruturar uma API REST profissional com FastAPI
- Integrar banco de dados relacional com SQLAlchemy e Alembic
- Implementar autenticação e autorização com JWT
- Escrever testes automatizados com Pytest
- Dockerizar a aplicação e trabalhar com PostgreSQL
- Configurar CI/CD com GitHub Actions
- Fazer deploy no Fly.io

**Nível:** Iniciante → Intermediário

---

## Aulas do Curso

| Aula | Conteúdo |
|------|----------|
| 01 | Configuração do ambiente |
| 02 | Introdução ao desenvolvimento WEB |
| 03 | Estruturando o projeto e criando rotas CRUD |
| 04 | Configurando o banco de dados com Alembic |
| 05 | Integrando o banco de dados à API |
| 06 | Autenticação e Autorização com JWT |
| 07 | Refatorando a estrutura do projeto |
| 08 | Tornando o projeto assíncrono |
| 09 | Tornando o sistema de autenticação robusto |
| 10 | Criando rotas CRUD para gerenciamento de tarefas |
| 11 | Dockerizando a aplicação e introduzindo o PostgreSQL |
| 12 | Automatizando os testes com integração contínua |
| 13 | Fazendo o deploy no Fly.io |

---

## Tech Stack

| Tecnologia | Versão | Descrição |
|---|---|---|
| Python | 3.13 | Linguagem principal |
| FastAPI | 0.115+ | Framework web de alta performance |
| Pydantic | 2.0+ | Validação de dados e schemas |
| SQLAlchemy | 2.0+ | ORM para persistência de dados |
| Alembic | latest | Gerenciamento de migrações |
| PostgreSQL | 15+ | Banco de dados relacional |
| Pytest | latest | Testes automatizados |
| Docker | 24+ | Conteinerização |
| GitHub Actions | — | CI/CD |

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

```
Python >= 3.12
Docker >= 24
```

---

## Como instalar e rodar

**1. Clone o repositório**

```bash
git clone https://github.com/CaioVHilario/fast_zero.git
cd fast_zero
```

**2. Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

**3. Suba a aplicação com Docker**

```bash
docker-compose up --build
```

**4. Acesse a documentação interativa (swagger)**

```
http://127.0.0.1:8000/docs
```

**5. Acesse a documentação**

```
http://127.0.0.1:8000/redoc
```

**Parar a aplicação:**

```bash
docker-compose down
```

---

## Testes e qualidade de código

```bash
# Formatar o código
task format

# Rodar os testes com cobertura
task test
```

Os relatórios de cobertura estarão disponíveis em: `htmlcov/index.html`

---

## Links úteis

- [Curso FastAPI do Zero](https://fastapidozero.dunossauro.com/)
- [Canal Live de Python](https://www.youtube.com/@Dunossauro)
- [Documentação oficial do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do SQLAlchemy](https://docs.sqlalchemy.org/)

---

## Créditos

Projeto desenvolvido como parte do curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/), ministrado por **Eduardo Mendes** na [Live de Python](https://www.youtube.com/@Dunossauro).

O material do curso está licenciado sob [Creative Commons BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/).
