import datetime
from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
)

from base_models import BaseModel


class Departments(BaseModel):
    """Виды департаментов."""
    name = CharField(max_length=64, unique=True)
    permissions = TextField(null=True)


class UserRole(BaseModel):
    """Виды ролей юзеров."""
    name = CharField(max_length=30, unique=True)


class User(BaseModel):
    """Основная таблица по юзерам"""
    name = CharField(max_length=64)
    surname = CharField(max_length=64)
    email = CharField(max_length=64, unique=True)
    password = CharField()
    department = ForeignKeyField(Departments)
    role = ForeignKeyField(UserRole, null=True, default=1)
    mobile_number = CharField(max_length=30, null=True)
    last_login = DateTimeField(null=True, formats=['%d-%m-%Y %H:%M:%S'])
    is_active = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    profile_picture = CharField(max_length=255, null=True)
    date_joined = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('surname', 'department',)
