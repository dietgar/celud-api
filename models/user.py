from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

logins = Table("logins", meta,
               Column("id_login", Integer, primary_key=True, autoincrement=True),
               Column("user_name", String(255), nullable=False),
               Column("user_mail", String(255), nullable=False),
               Column("password", String(255), nullable=False))

meta.create_all(engine)
