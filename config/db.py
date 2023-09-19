from sqlalchemy import create_engine, MetaData

engine = create_engine(
    "mysql+pymysql://doadmin:AVNS_vWpE7ovVIRG32rWgrAM@salud-movil-test-do-user-14619953-0.b.db.ondigitalocean.com:25060/salud-movil")

meta = MetaData()
