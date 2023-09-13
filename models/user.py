from sqlalchemy import Table, Column
from datetime import date
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine

users = Table("users", meta,
              Column("id_users", Integer, primary_key=True, autoincrement=True),
              Column("first_name", String(255)),
              Column("last_name", String(255)),
              Column("age", Integer),
              Column("height", Float),
              Column("weight", Float))

login = Table("login", meta,
              Column("id_login", Integer, primary_key=True, autoincrement=True),
              Column("user_name", String(255)),
              Column("user_mail", String(255)),
              Column("password", String(255)))

user_contact = Table("user_contact", meta,
                     Column("id_contact", Integer, primary_key=True, autoincrement=True))

medical_user_info = Table("medical_user_info", meta,
                          Column("id_info", Integer, primary_key=True,
                                 autoincrement=True),
                          Column("allergy", String(255)),
                          Column("chronic_disease", String(255)),
                          Column("active_drugs", String(255)))

user_adress = Table("user_adress", meta,
                    Column("id_adress", Integer,
                           primary_key=True, autoincrement=True),
                    Column("adress", String(255)))

appointments_user = Table("appointments_user", meta,
                          Column("id_appointment", Integer,
                                 primary_key=True, autoincrement=True),
                          Column("appointment_date", String(255)),
                          Column("appointment_place", String(255)),
                          Column("clinic_name", String(255)))

meta.create_all(engine)
