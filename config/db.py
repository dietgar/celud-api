from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://root:password@host:port/db_name")

meta = MetaData()
