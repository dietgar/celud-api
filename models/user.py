from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine

users = Table("user", meta,
              Column("id_users", Integer, primary_key=True, autoincrement=True),
              Column("first_name", String(255)),
              Column("last_name", String(255)),
              Column("age", Integer),
              Column("height", Float),
              Column("weight", Float))

meta.create_all(engine)
