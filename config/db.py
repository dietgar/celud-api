from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://root:josegarcia99@localhost:3306/salud_movil")

meta = MetaData()
