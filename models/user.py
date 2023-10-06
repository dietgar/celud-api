from sqlalchemy import Table, Column, Integer, String, Date, Float, Boolean, ForeignKey
from config.db import meta, engine


user = Table("user", meta,
             Column("id_user", Integer, primary_key=True, autoincrement=True),
             Column("first_name", String(50), nullable=False),
             Column("last_name", String(50), nullable=False),
             Column("phone_number", String(15), nullable=False),
             Column("username", String(50), nullable=False),
             Column("email", String(50), nullable=False),
             Column("password", String(255), nullable=False)
             )

user_data = Table("user_data", meta,
                  Column("id_user_data", Integer,
                         primary_key=True, autoincrement=True),
                  Column("id_user", Integer, ForeignKey("user.id_user")),
                  Column("height", Float, nullable=False),
                  Column("weight", Float, nullable=False),
                  Column("birth_date", Date, nullable=False),
                  Column("blood_type", String(5), nullable=False),
                  Column("status_", Boolean, nullable=False)
                  )

user_contact = Table("user_contact", meta,
                     Column("id_user_contact", Integer,
                            primary_key=True, autoincrement=True),
                     Column("id_user", Integer, ForeignKey("user.id_user")),
                     Column("name", String(50), nullable=False),
                     Column("relationship", String(50), nullable=False),
                     Column("phone_number", String(15), nullable=False)
                     )


reminder = Table("reminder", meta,
                 Column("id_reminder", Integer,
                        primary_key=True, autoincrement=True),
                 Column("id_user", Integer, ForeignKey('user.id_user')),
                 Column("date_", Date, nullable=False),
                 Column("time_", String(5), nullable=False),
                 Column("reminder_text", String(100), nullable=False),
                 Column("status_", Boolean, nullable=False)
                 )


drug = Table("drug", meta,
             Column("id_drug", Integer, primary_key=True, autoincrement=True),
             Column("id_user", Integer, ForeignKey("user.id_user")),
             Column("drug_name", String(50), nullable=False),
             )


allergy = Table("allergy", meta,
                Column("id_allergy", Integer,
                       primary_key=True, autoincrement=True),
                Column("id_user", Integer, ForeignKey("user.id_user")),
                Column("allergy_name", String(50), nullable=False),
                )


chronic_diseases = Table("chronic_diseases", meta,
                         Column("id_chronic_disease", Integer,
                                primary_key=True, autoincrement=True),
                         Column("id_user", Integer,
                                ForeignKey("user.id_user")),
                         Column("disease_name", String(50), nullable=False),
                         )


user_drug = Table("user_drug", meta,
                  Column("id_user_drug", Integer,
                         primary_key=True, autoincrement=True),
                  Column("id_user", Integer, ForeignKey("user.id_user")),
                  Column("id_drug", Integer, ForeignKey("drug.id_drug")),
                  Column("status_", Boolean, nullable=False)
                  )


user_allergy = Table("user_allergy", meta,
                     Column("id_user_allergy", Integer,
                            primary_key=True, autoincrement=True),
                     Column("id_user", Integer, ForeignKey("user.id_user")),
                     Column("id_allergy", Integer,
                            ForeignKey("allergy.id_allergy")),
                     Column("status_", Boolean, nullable=False)
                     )


user_chronic_diseases = Table("user_chronic_diseases", meta,
                              Column("id_user_chronic_disease", Integer,
                                     primary_key=True, autoincrement=True),
                              Column("id_user", Integer,
                                     ForeignKey('user.id_user')),
                              Column("id_chronic_disease", Integer, ForeignKey(
                                  "chronic_diseases.id_chronic_disease")),
                              Column("status_", Boolean, nullable=False)
                              )


user_address = Table("user_address", meta,
                     Column("id_user_address", Integer,
                            primary_key=True, autoincrement=True),
                     Column("id_user", Integer, ForeignKey("user.id_user")),
                     Column("address", String(100), nullable=False),
                     )


appointment = Table("appointment", meta,
                    Column("id_appointment", Integer,
                           primary_key=True, autoincrement=True),
                    Column("id_user", Integer, ForeignKey("user.id_user")),
                    Column("appointment_date", Date, nullable=False),
                    Column("appointment_place", String(50), nullable=False),
                    Column("clinic_name", String(50)),
                    Column("status_", Boolean, nullable=False)
                    )


info_appointment = Table("info_appointment", meta,
                         Column("id_info_appointment", Integer,
                                primary_key=True, autoincrement=True),
                         Column("id_appointment", Integer, ForeignKey(
                             "appointment.id_appointment")),
                         Column("blood_pressure", String(20)),
                         Column("temperature", String(20)),
                         Column("heart_rate", String(20)),
                         Column("weight", String(20)),
                         Column("next_appointment_date", Date, nullable=False),
                         Column("observation", String(100))
                         )


meta.create_all(engine)
