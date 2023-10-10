# Celud-API - Instalación y tutorial

## Guía de instalación

## Se debe tener Python 3 y MySQL instalado

### Se recomienda usar la terminal Git Bash en el caso de usar Windows*

- Abrir una terminal

- Dirigirse al directorio donde se va a clonar el repositorio

- Clonar el repositorio:

  `git clone https://github.com/dietgar/celud-api.git`

- Entrar dentro del repositorio

  `cd celud-api`

- Cambiar el archivo `config/db.py` con la información correspondiente a tu instalación de MySQL

- Crear el **entorno virtual**:

  `python -m venv nombre_del_entorno_virtual`

  > Es recomendable nombrar al entorno virtual como venv, de la siguiente manera:

  `python -m venv venv`

- Activar el entorno virtual

  **Para Windows**

  `.\nombre_del_entorno_virtual\Scripts\activate`

  `.\venv\Scripts\activate`

  **Para Linux**

  `source nombre_del_entorno_virtual/bin/activate`

  `source venv/bin/activate`

  **Git Bash en Windows**
  
  `source nombre_del_entorno_virtual/Scripts/activate`

  `source venv/Scripts/activate`

- Instalar las dependencias

  `pip install -r requeriments.txt`

- Levantar el servidor uvicorn

  `uvicorn app:app --reload`

  > Esto levanta el servidor en localhost:8000

## Tutorial

## Crear un usuario

- POST `/users/register` > Agregar un usuario
```json
    {
      "first_name": "string",
      "last_name": "string",
      "username": "string",
      "email": "string",
      "password": "string"
    }
```
- POST `/users/login` > Iniciar sesión

    {
      "email": "string",
      "password": "string"
    }

- POST `/users/personal-data/{user_id}` > Agregar datos personales mediante id

    > Por ejemplo: /users/personal-data/1

    {
      "height": 0,
      "weight": 0,
      "birth_date": "string",
      "blood_type": "string",
      "status_": true
    }

- POST `/users/user-contact/{user_id}` > Agregar contacto de emergencia mediante id

    > Por ejemplo: /users/user-contact/1

    {
      "name": "string",
      "relationship": "string",
      "phone_number": "string"
    }

- POST `/users/reminder/{user_id}` > Agregar un recordatorio

    > Por ejemplo: /users/reminder/1

    {
      "date_": "string",
      "time_": "string",
      "reminder_text": "string",
    }

- POST `/users/address/{user_id}` > Agregar una dirección

    > Por ejemplo: /users/address/1

    {
      "address": "string"
    }

- POST `/users/appointment/{user_id}` > Agrega una cita

    > Por ejemplo: /users/appointment/1

    {
      "appointment_date": "string",
      "appointment_place": "string",
      "clinic_name": "string"
    }

- POST `/users/info-appointments/{user_id}` > Agrega información de una cita

    > Por ejemplo: /users/info-appointments/1

    {
      "blood_pressure": "string",
      "temperature": "string",
      "heart_rate": "string",
      "weight": "string",
      "next_appointment_date": "string",
      "observation": "string"
    }

- POST `/users/drug/{user_id}` > Agregar un medicamento

    > Por ejemplo: /users/drug/1

    {
      "drug_name": "string"
    }

- POST `/users/allergy/{user_id}` >  Agregar una alergia

    > Por ejemplo: /users/allergy/1

    {
      "allergy_name": "string"
    }

- POST `/users/chronic-disease/{user_id}` > Agregar una enfermedad crónica

    > Por ejemplo: /users/chronic-disease/1

    {
      "disease_name": "string"
    }
