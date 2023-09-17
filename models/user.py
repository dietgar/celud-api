from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

logins = Table("logins", meta,
               Column("id_login", Integer, primary_key=True, autoincrement=True),
               Column("user_name", String(255)),
               Column("user_mail", String(255)),
               Column("password", String(255)))

meta.create_all(engine)
