from schemas.user_schema import Register
from datetime import datetime
from config.db import engine
from models.user import user
import time
import re


def format_string(name):
    delete_white_spaces = name.replace(" ", "")
    name_to_minus = delete_white_spaces.casefold()
    name_to_capitalize = name_to_minus.capitalize()
    return name_to_capitalize


def format_date(date):
    birth_date = datetime.strptime(date, "%d/%m/%Y").date()
    return birth_date


def validate_time(time_):
    if time.strptime(time_, "%H:%M"):
        return True


def validate_date(date):
    pattern = r'^\d{1,2}/\d{1,2}/\d{4}$'
    result = re.search(pattern, date)
    if result:
        return True
    return False


def validate_phone_number(phone_number):
    pattern = r'^[0-9]{8}$'
    if re.match(pattern, phone_number):
        return True
    return False


def validate_string(name):
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


def validate_string2(name):
    if len(name) > 0 and len(name) < 50:
        if re.match("^[a-zA-Z.]+$", name):
            return True
    return False


def exist_phone_number(phone_number):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.phone_number == phone_number)).first()
        if result is not None:
            return True
        return False


def validate_blood_pressure(blood_pressure):
    pattern = r'^\d{1,3}/\d{1,3}$'
    if re.match(pattern, blood_pressure):
        return True
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
        if validate_string(data_user.first_name):
            counter += 1
        if validate_string(data_user.last_name):
            counter += 1
        if validate_username(data_user.username):
            counter += 1
        if validate_email(data_user.email):
            counter += 1
        if validate_secure_password(data_user.password):
            counter += 1
        if counter == 5:
            return True

    except:
        return {
            "detail": "Ha ocurrido un error inesperado"
        }
