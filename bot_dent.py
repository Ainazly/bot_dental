
from telebot import TeleBot, types
from telebot.types import Message
from config import *
from models import User, Appointment
from db import my_cursor, db
import mysql.connector
import peewee
import datetime


from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

bot = TeleBot(TOKEN)
# calendar1 =CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.datetime.now()


@bot.message_handler(commands=["start"])
def send_welcome_message(message):
    text = f"""Здравствуйте!
        Вас приветствует БОТ, для записи на прием к стоматологу!
        Напишите ИФО, номер вашего номера и выберите удобное для вас время. """
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    continue_step = InlineKeyboardButton(f"Записаться на прием", callback_data="appointment")
    markup.add(continue_step)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "appointment")
def add_user(message):
    msg = bot.send_message(message.from_user.id, "Здравствуйте, для записи на прием к стоматологу, введите ваше ФИО)")
    bot.register_next_step_handler(msg, process_fullname)


def process_fullname(message):
    global full_name
    try:
        full_name = message.text
        msg = bot.send_message(message.chat.id, 'Имя сохранено, введите номер телефона')
        bot.register_next_step_handler(msg, get_phone)

    except Exception as e:
        bot.reply_to(message, 'ooooops, Ваше имя не сохранена')


def get_phone(message):
    try:
        tg_user_id = str(message.from_user.id)
        phone_number = message.text

        msg = bot.send_message(message.chat.id, f"Вы почти записались на прием, \n осталось выбрать время и дату")
        User.create(tg_user_id=tg_user_id, full_name=full_name, phone_number=phone_number)
        bot.register_next_step_handler(msg, view_calendar)

    except Exception as e:
        bot.reply_to(message, 'oooops, Ошибка в сохранений данных')


def view_calendar(message):
    now = datetime.datetime.now()
    chat_id = message.chat.id
    date = (now.year, now.month)
    current_show_dates[chat_id] = date
    markup = create_calendar(now.year, now.month)
    bot.send_message(message.chat.id, "Выберите дату", reply_markup=markup)
    bot.answer_callback_query(message.call.id, text="Д"
                                                    "ата выбрана")



bot.infinity_polling()

