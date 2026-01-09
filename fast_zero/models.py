from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

# função para registrar no banco as tabelas
table_registry = registry()


# criando uma dataclass que já registra no banco a tabela (table_registre)
@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'  # o nome da tabela do db é users

    # Mapped mapeia as informações para o banco de dados
    # init=False para que o banco crie id sozinho
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )  # server_default= para o banco preencer com a hora atual
