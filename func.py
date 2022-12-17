from telebot import *
from BD_test import *
bot = telebot.TeleBot("5684813261:AAFh-vNDAaWZPH3diBsD5NPAhi8Qw-MKzas")

back_part = 0

def consumption_water(message):
    global back_part
    if (message.text == "Расход воды"):
        #markup =types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
        btn1 = types.KeyboardButton ("Расход воды за месяц")
        btn2 = types.KeyboardButton ("Расход воды за всё время")
        btn3 = types.KeyboardButton ("Назад")
        markup.add (btn1, btn2, btn3)
        back_part = 1
        bot.reply_to(message, "Я сделатъ" ,reply_markup = markup )
        #bot.send_message( message.from_user.id , "Привет! Я твой бот-помощник. Готов показать твои расходы за месяц!", reply_markup = markup)
def consumption_electricity(message):
    global back_part
    if (message.text == "Расход электричества"):
        #markup =types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
        btn1 = types.KeyboardButton ("Расход электричества за месяц")
        btn2 = types.KeyboardButton ("Расход электричества за всё время")
        btn3 = types.KeyboardButton ("Назад")
        markup.add (btn1, btn2, btn3)
        back_part = 2
        bot.reply_to(message, "Я сделатъ" ,reply_markup = markup )
def back(message):
    if ((message.text == "Назад" and back_part == 1) or (message.text == "Назад" and back_part == 2)):
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
        btn1 = types.KeyboardButton ("Расход воды")
        btn2 = types.KeyboardButton ("Расход электричества")
        markup.add (btn1, btn2)
        bot.reply_to(message, "Есть!" ,reply_markup = markup )
def consumption_electricity_month(message):
    if (message.text == "Расход электричества за месяц"):
        #print("Error1")
        data = get_data_from_BD()
        #print (data)
        bot.send_message (message.from_user.id, "Расход электричества - {0} кВт".format(data[2]))
def registration_name(message):
    if message.text == "Регистрация пользователя":
        bot.send_message( message.from_user.id , "Придумай себе логин и напиши его мне")
        bot.register_next_step_handler(message, insert_name_to_BD)



if __name__ == "__main__":
    print("Hi")