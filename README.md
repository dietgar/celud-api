# Celud-API - Instalación y tutorial

## Guía de instalación

## Se debe tener Python 3 y MySQL instalado

### Se recomienda usar la terminal Git Bash en el caso de usar Windows\*

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

## Endpoints

### Crear un usuario

- POST `/users/register` > Agregar un usuario

```json
{
  "data": {
    "first_name": "string",
    "last_name": "string",
    "username": "string",
    "email": "string",
    "password": "string"
  }
}
```

### Iniciar sesión

- POST `/users/login` > Iniciar sesión

```json
{
  "data": {
    "email": "string",
    "password": "string"
  }
}
```

- POST `/user/medicaments/{user_id}` > Agregar medicamento mediante el ID del usuario

  > Por ejemplo: /user/medicaments/1

```json
{
  "data": {
    "name": "string",
    "description": "string"
  },
  "medicament_data": {
    "cantity": "string",
    "frecuency": "string",
    "duration": "string"
  }
}
```

- POST `/user/reminder-medicament/{user_id}/{medicament_id}` > Agregar recordatorio de medicamento mediante ID de usuario y ID de medicamento

  > Por ejemplo: /user/reminder-medicament/1/1

```json
{
  "data": {
    "text": "string",
    "date_": "DD/MM/YYYY",
    "time_": "HH:MM"
  }
}
```

- POST `/users/measurements/{user_id}` > Agregar la medición mediante el ID del usuario

  > Por ejemplo: /users/measurements/1

```json
{
  "data": {
    "weight": 0,
    "glycemia": "string",
    "blood_presure": "120/80" // Formato de presión arterial
  }
}
```

- POST `/users/appointment/{user_id}` > Agregar una cita mediante el ID del usuario

  > Por ejemplo: /users/appointment/1

```json
{
  "data": {
    "date_": "DD/MM/YYYY",
    "time_": "HH:MM",
    "place": "string",
    "doctor": "string"
  }
}
```

- POST `/users/reminder-appointment/{user_id}/{appointment_id}` > Agregar un recordatorio de cita mediante el ID del usuario y el ID de la cita

  > Por ejemplo: /users/reminder-appointment/1/1

```json
{
  "data": {
    "text": "string",
    "date_": "DD/MM/YYYY",
    "time_": "HH:MM"
  }
}
```
