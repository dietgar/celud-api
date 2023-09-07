from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine

# seria bueno definir una tabla para los roles

users = Table("users", meta,
              Column("id_users", Integer, primary_key=True, autoincrement=True),
              Column("first_name", String(255)),
              Column("last_name", String(255)),
              Column("age", Integer),
              #   en lugar de age que sea birthday de tipo Date
              # seria bueno agregar un campo para el tipo de sangre
              Column("height", Float),
              Column("weight", Float))

login = Table("login", meta,
              Column("id_login", Integer, primary_key=True, autoincrement=True),
              Column("user_name", String(255)),
              Column("user_mail", String(255)),
              Column("password", String(255)))

# deberian tener una relacion con users
user_contact = Table("user_contact", meta,
                     Column("id_contact", Integer, primary_key=True, autoincrement=True))

medical_user_info = Table("medical_user_info", meta,
                          Column("id_info", Integer, primary_key=True,
                                 autoincrement=True),
                          Column("allergy", String(255)),
                          # allergy es una tabla nueva, diseases tambien y drugs tambien
                          Column("chronic_disease", String(255)),
                          Column("active_drugs", String(255)))

# sintomas -> enfermedad
# medicamento -> enfermedad


user_adress = Table("user_adress", meta,
                    Column("id_adress", Integer,
                           primary_key=True, autoincrement=True),
                    Column("adress", String(255)))
# deberia tener una relacion con el usuario

appointments_user = Table("appointments_user", meta,
                          Column("id_appointment", Integer,
                                 primary_key=True, autoincrement=True),
                          Column("appointment_date", String(255)),
                          Column("appointment_place", String(255)),
                          Column("clinic_name", String(255)))

# va a ser necesario guardar los resultados de la visita medica ->
# seria bueno guardar: frecuencia cardiaca, presion, peso

# saber si van a guardar los doctores o no?
# van a tener un catalogo de las clinicas? -> clinica es una nueva tabla
# tener un catalogo de la informacion de las clinicas, teniendo la direccion
# informacion sobre las especialidades de la clinica
# seria bueno por ejemplo hacer una especie de rate sobre las clinicas o doctores
# tener informacion sobre la especialidad a la que se relaciona la cita

# seria bueno crear una especie de calendario o recordatorios para los medicamentos


# normalmente no se suelen elimminar los datos, sino que se pasan a algun estado inactivo ->
# todas las tablas deberian de tener una columna llamada status o estado
meta.create_all(engine)
