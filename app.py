from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from litestar import Litestar, get, post
from litestar.contrib.sqlalchemy.plugins import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)


class Base(DeclarativeBase):
    pass


class ToDo(Base):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    user_id: Mapped[int]

@post("/todo")
async def create_todos(data: ToDo, db_session: AsyncSession) -> ToDo:
    async with db_session.begin():
        db_session.add(data)
        return data
    

@get("/todo")
async def get_todos(db_session: AsyncSession) -> list[ToDo]:
    async with db_session.begin():
        query = select(ToDo)
        result = await db_session.execute(query)
        return result.scalar().all()


db_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///db.sqlite",
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)

app = Litestar(
    [create_todos, get_todos],
    plugins=[SQLAlchemyPlugin(db_config)],
)
