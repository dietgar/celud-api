# Guía de instalación:

**Se debe tener Python 3 y MySQL instalado**
_Se recomienda usar la terminal Git Bash en el caso de usar Windows_

- Abrir una terminal

- Dirigirse al directorio donde se va a clonar el repositorio

- Clonar el repositorio

  `git clone https://github.com/dietgar/celud-api.git`
  `cd celud-api`

- Cambiar el archivo `config/db.py` con la información correspondiente a tu instalación de MySQL

- Crear el **entorno virtual**:

  `python -m venv nombre_del_entorno_virtual`

  > Es recomendable nombrar al entorno virtual como venv

- Activar el entorno virtual

  **Para Windows**
  `.\nombre_del_entorno_virtual\Scripts\activate`

  **Para Linux**
  `source nombre_del_entorno_virtual/bin/activate`

- Instalar las dependencias

  `pip install -r requeriments.txt`

- Levantar el servidor uvicorn

  `uvicorn app:app --reload`

  > Esto levanta el servidor en localhost:8000
