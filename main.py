import telebot
from func import *
from telebot import types

bot = telebot.TeleBot("5684813261:AAFh-vNDAaWZPH3diBsD5NPAhi8Qw-MKzas")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
    btn1 = types.KeyboardButton ("Зарегистрированный пользователь")
    btn2 = types.KeyboardButton ("Регистрация пользователя")
    markup.add (btn1, btn2)
    bot.send_message( message.from_user.id , "Привет! Я твой бот-помощник. Готов показать твои расходы. Но сначала давай залогинемся")
    bot.send_message( message.from_user.id , "Выбери тип пользовтаеля", reply_markup = markup)
    

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message( message.from_user.id , "Chem i moge pomoch?")

@bot.message_handler(func = lambda message: True)
def main(message):
    consumption_water(message)
    consumption_electricity(message)
    consumption_electricity_month(message)
    registration_name(message)
    back(message)
'''@bot.message_handler(content_types = ['text'])
def func(message):
    if (message.text == ""):
        print("ERROR")
        #markup =types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard= True) 
        btn1 = types.KeyboardButton ("")
        btn3 = types.KeyboardButton ("Назад")
        markup.add (btn1, btn3)
        bot.reply_to(message, "Быдло" ,reply_markup = markup )'''

bot.infinity_polling()