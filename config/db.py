from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://user:password@host:port/db_name")

meta = MetaData()

conn = engine.connect()
