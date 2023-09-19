from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table("users", meta,
              Column("id", Integer, primary_key=True, autoincrement=True),
              Column("user_name", String(255), nullable=False),
              Column("user_mail", String(255), nullable=False),
              Column("user_password", String(255), nullable=False))

meta.create_all(engine)
