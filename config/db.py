from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://root:Rotting7-Hankie3@localhost:3306/system_health_mobile")

meta = MetaData()
