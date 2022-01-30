import re
import telebot
from telebot import types #кнопки

# Telegram your token
bot = telebot.TeleBot("5294370282:AAHB6mM8swgEsgj4-wHHMNF72c5eHtGbVOw")

user_data = {}

class User:
    def __init__(self, city):
        self.city = city

        keys = ['kateg', 'fam_imia_otch',
                'phone', 'fot',
                'geo', 'opis']

        for key in keys:
            self.key = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте " + message.from_user.first_name + ", для того ,что бы продолжить, напишите боту /Sostavitim")

@bot.message_handler(commands=['Sostavitim'])
def zaiavka(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("Пробка на дороге")
    item2 = types.KeyboardButton("Нарушение ПДД")
    item3 = types.KeyboardButton("Другое")
    markup.add(item1, item2, item3)
    msg = bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup)
    bot.register_next_step_handler(msg, fam_imia_otch)

def fam_imia_otch(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, "Введите ФИО", reply_markup=markup)
        bot.register_next_step_handler(msg, phone)
    except Exception as e:
        msg = bot.reply_to(message, 'Введите нужную категорию')
        bot.register_next_step_handler(msg, fam_imia_otch)

def phone(message):
    try:
        full_name = message.text
        if len(full_name.split()) != 3:
            raise
        if not full_name.replace(' ', '').isalpha():
            raise
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, "Введите номер телефона (071XXXXXXX)")
        bot.register_next_step_handler(msg, fot)
    except Exception as e:
        msg = bot.reply_to(message, 'Введите корректное ФИО')
        bot.register_next_step_handler(msg, phone)

def fot(message):
    try:
        int(message.text)
        phone_number = message.text
        if re.match(r'^071\d{7}$', phone_number) is None:
            message.answer('Введите корректный номер телефона')
            return

        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text

        msg = bot.send_message(message.chat.id, "Отправьте фотографии")
        bot.register_next_step_handler(msg, opis)
    except Exception as e:
        msg = bot.reply_to(message, 'Введите корректный номер телефона')
        bot.register_next_step_handler(msg, fot)

def opis(message):
    try:
        if message.content_type == 'photo':
            user_id = message.from_user.id
            user = user_data[user_id]
            user.photo_id = message.photo[-1].file_id

            msg = bot.send_message(message.chat.id, "Введите описание ")
            bot.register_next_step_handler(msg, geo)
        else:
            bot.reply_to(message, 'Отправьте фотографии')
            fot(message)
    except Exception as e:
        bot.reply_to(message, "")

def geo(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, "Введите адрес")
        bot.register_next_step_handler(msg, vuvod1)
    except Exception as e:
        bot.reply_to(message, '')

def vuvod1(message):
    chat_id = message.chat.id
    user = user_data[chat_id]
    user.carDate = message.text
    bot.send_message(message.chat.id, "Заявка отправлена " + message.from_user.first_name, parse_mode="Markdown")


# RUN
bot.polling(none_stop=True)
