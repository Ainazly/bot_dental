import peewee
from db import db


class User(peewee.Model):
    tg_user_id = peewee.CharField()
    full_name = peewee.CharField()
    phone_number = peewee.CharField()

    class Meta:
        database = db


class Appointment(peewee.Model):
    user_id = peewee.ForeignKeyField(User, on_delete="CASCADE")
    date = peewee.DateField()
    time = peewee.TimeField

    class Meta:
        database = db


if not User.table_exists():
    User.create_table()
if not Appointment.table_exists():
    Appointment.create_table()