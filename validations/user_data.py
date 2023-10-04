from schemas.user_schema import Register
from config.db import engine
from models.user import user
import re


def format_name(name):
    try:
        delete_white_spaces = name.replace(" ", "")
        name_to_minus = delete_white_spaces.casefold()
        name_to_capitalize = name_to_minus.capitalize()
        return name_to_capitalize
    except:
        return {
            "detail": "Ha ocurrido un error al momento de formatear el nombre"
        }


def is_empty(name):
    if len(name) == 0:
        return True


def validate_names(name):
    try:
        if len(name) > 0 and len(name) < 50:
            number = False
            digit = False
            if re.search(r'\d', name):
                number = True
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', name):
                digit = True
            if not digit and number:
                return False
            return True
    except:
        return False


def exist_username(username):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.username == username)).first()
        if result is not None:
            return True
        return False


def validate_username(username):
    if len(username) > 3 and len(username) < 15:
        if re.match(r'^[a-zA-Z0-9_-]+$', username):
            return True


def exist_email(email):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.email == email)).first()
        if result is not None:
            return True
        return False


def validate_email(email):
    if len(email) > 0 and len(email) < 50:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        result = re.search(pattern, email)
        if result:
            return True


def validate_secure_password(password):
    mayus = False
    minus = False
    number = False
    digit = False
    if len(password) >= 8 and len(password) < 50:
        if re.search(r'[A-Z]', password):
            mayus = True
        if re.search(r'[a-z]', password):
            minus = True
        if re.search(r'\d', password):
            number = True
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            digit = True
        if mayus and minus and number and digit:
            return True


def validate_data_user(data_user: Register):
    try:
        counter = 0
        if validate_names(data_user.first_name):
            print(data_user.first_name)
            counter += 1
        if validate_names(data_user.middle_name):
            print(data_user.middle_name)
            counter += 1
        if is_empty(data_user.middle_name):
            print(data_user.middle_name)
            counter += 1
        if validate_names(data_user.last_name):
            print(data_user.last_name)
            counter += 1
        if validate_names(data_user.second_last_name):
            print(data_user.second_last_name)
            counter += 1
        if is_empty(data_user.second_last_name):
            print(data_user.second_last_name)
            counter += 1
        if validate_username(data_user.username):
            print(data_user.username)
            counter += 1
        if validate_email(data_user.email):
            print(data_user.email)
            counter += 1
        if validate_secure_password(data_user.password):
            print(data_user.password)
            counter += 1
        print("Contador: ", counter)
        if counter == 7:
            return True

    except:
        return {
            "detail": "Ha ocurrido un error inesperado"
        }
