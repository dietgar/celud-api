from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey
from config.db import meta, engine


# Tabla user
user = Table("user", meta,
             Column("id", Integer, primary_key=True, autoincrement=True),
             Column("first_name", String(50), nullable=False),
             Column('middle_name', String(50), nullable=False),
             Column('last_name', String(50), nullable=False),
             Column('second_last_name', String(50), nullable=False),
             Column('username', String(50), nullable=False),
             Column('email', String(50), nullable=False),
             Column('password', String(255), nullable=False)
             )

# user_data = Table("user_data", meta,
#                   Column('birth_date', Date, nullable=False),
#                   Column('heigth', Float, nullable=False),
#                   Column('weigth', Float, nullable=False),
#                   # Column('id_blood_type', Integer, ForeignKey(
#                   #    'blood_type.id_blood_type')),
#                   Column('status_', Boolean, nullable=False)
#                   )

# Tabla blood_type
# blood_type = Table('blood_type', meta,
#                    Column('id_blood_type', Integer,
#                           primary_key=True, autoincrement=True),
#                    Column('blood_type', String(3), unique=True, nullable=False)
#                    )


# Tabla user_contact
# user_contact = Table('user_contact', meta,
#                      Column('id_user_contact', Integer,
#                             primary_key=True, autoincrement=True),
#                      Column('id_user', Integer, ForeignKey('user.id_user')),
#                      Column('phone_number', String(9), nullable=False)
#                      )

# Tabla reminder
# reminder = Table('reminder', meta,
#                  Column('id_reminder', Integer,
#                         primary_key=True, autoincrement=True),
#                  Column('id_user', Integer, ForeignKey('user.id_user')),
#                  Column('date_', Date, nullable=False),
#                  Column('time_', String(5), nullable=False),
#                  Column('reminder', String(100), nullable=False),
#                  Column('status_', Boolean, nullable=False)
#                  )

# Tabla drug
# drug = Table('drug', meta,
#              Column('id_drug', Integer, primary_key=True, autoincrement=True),
#              Column('drug', String(60), nullable=False)
#              )

# Tabla allergy
# allergy = Table('allergy', meta,
#                 Column('id_allergy', Integer,
#                        primary_key=True, autoincrement=True),
#                 Column('allergy', String(70), nullable=False)
#                 )

# Tabla chronic_diseases
# chronic_diseases = Table('chronic_diseases', meta,
#                          Column('id_chronic_diseases', Integer,
#                                 primary_key=True, autoincrement=True),
#                          Column('chronic_diseases', String(70), nullable=False)
#                          )

# Tabla user_drug
# user_drog = Table('user_drog', meta,
#                   Column('id_user_drug', Integer,
#                          primary_key=True, autoincrement=True),
#                   Column('id_user', Integer, ForeignKey('user.id_user')),
#                   Column('id_drug', Integer, ForeignKey('drug.id_drug')),
#                   Column('status_', Boolean, nullable=False)
#                   )

# Tabla user_allergy
# user_allergy = Table('user_allergy', meta,
#                      Column('id_user_allergy', Integer,
#                             primary_key=True, autoincrement=True),
#                      Column('id_user', Integer, ForeignKey('user.id_user')),
#                      Column('id_allergy', Integer,
#                             ForeignKey('allergy.id_allergy')),
#                      Column('status_', Boolean, nullable=False)
#                      )

# Tabla user_chronic_diseases
# user_chronic_diseases = Table('user_chronic_diseases', meta,
#                               Column('id_user_chronic_diseases', Integer,
#                                      primary_key=True, autoincrement=True),
#                               Column('id_user', Integer,
#                                      ForeignKey('user.id_user')),
#                               Column('id_chronic_diseases', Integer, ForeignKey(
#                                   'chronic_diseases.id_chronic_diseases')),
#                               Column('status_', Boolean, nullable=False)
#                               )

# Tabla user_address
# user_address = Table('user_address', meta,
#                      Column('id_user_address', Integer,
#                             primary_key=True, autoincrement=True),
#                      Column('id_user', Integer, ForeignKey('user.id_user')),
#                      Column('address_', String(100), nullable=False)
#                      )

# Tabla appointment
# appointment = Table('appointment', meta,
#                     Column('id_appointment', Integer,
#                            primary_key=True, autoincrement=True),
#                     Column('id_user', Integer, ForeignKey('user.id_user')),
#                     Column('appointment_date', Date, nullable=False),
#                     Column('appointment_place', String(60), nullable=False),
#                     Column('clinic_name', String(50)),
#                     Column('status_', Boolean, nullable=False)
#                     )

# Tabla info_appointment
# info_appointment = Table('info_appointment', meta,
#                          Column('id_info_appointment', Integer,
#                                 primary_key=True, autoincrement=True),
#                          Column('id_appointment', Integer, ForeignKey(
#                              'appointment.id_appointment')),
#                          Column('blood_preasure', String(20)),
#                          Column('temperature', String(3)),
#                          Column('heart_rate', String(4)),
#                          Column('weigth', String(3)),
#                          Column('next_appointment_date', Date, nullable=False),
#                          Column('observation', String(100))
#                          )

# Crear todas las tablas en la base de datos
meta.create_all(engine)

# Asegurar que las FOREIGN KEYS estén habilitadas
# with engine.connect() as conn:
#     conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
