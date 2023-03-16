import telebot
import psycopg2

from telebot import types
from psycopg2 import Error

bot = telebot.TeleBot("5684813261:AAFh-vNDAaWZPH3diBsD5NPAhi8Qw-MKzas")
connection = psycopg2.connect (dbname = "Start", user = "postgres", password = "1", host = "localhost", port = "5432")
Back_counter = 0

#---------------------------------------------------
#---------START FUNCTION----------------------------
#---------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    insert_name_to_BD(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
    btn1 = types.KeyboardButton ("Ввести имя топика")
    markup.add (btn1)
    bot.send_message( message.from_user.id , "Привет! Я твой бот-помощник. Готов показать твои расходы. Но сначала давай подключимся к топику",reply_markup = markup)
  
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message( message.from_user.id , "Chem i moge pomoch?")

#---------------------------------------------------
#---------MAIN FUNCTION----------------------------
#---------------------------------------------------
@bot.message_handler(func = lambda message: True)
def main(message):
    consumption_water(message)
    insert_data_water(message)
    consumption_electricity(message)
    consumption_electricity_month(message)
    registration_topic(message)
    back(message)

#---------------------------------------------------
#---------FUNCTION WITH BOT-------------------------
#---------------------------------------------------

#---------Search id in DB---------------------------    
def search_nameid_in_dev(name): 
    #print(connection)
    try:
        cursor = connection.cursor()
        select_Query = "select u_name from dev_1 where u_name = '{0}'".format(name)
        cursor.execute(select_Query)
        records = cursor.fetchone()
        connection.commit()
        return records
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL из search_nameid_in_dev. Error = {0}".format(error))
    finally:
        if connection:
            print("Соединение с PostgreSQL закрыто из search_nameid_in_login") 

def insert_name_to_BD(name_id):
    try:
        check_name = search_nameid_in_dev(name_id)
        if check_name is None:
            cursor = connection.cursor()
            select_Query = "insert into dev_1 (u_name) values ('{0}')".format(name_id)
            cursor.execute(select_Query)
            connection.commit()


    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL в insert_name_to_BD. Error {0}",format(error))
    finally:
        if connection:
            print("Соединение с PostgreSQL закрыто из insert_name_to_BD")

#-------------------Получение имя топика-----------(сделать проверку топика из другой таблицы)     
      
def registration_topic(message):
    if message.text == "Ввести имя топика":
        msg = bot.send_message( message.from_user.id , "Напиши имя топика, к которому подключен модуль")
        bot.register_next_step_handler(msg, save_topic_BD)

def save_topic_BD(message):
    try:
        cursor = connection.cursor()
        select_Query = "update dev_1 set topic = '{0}' where u_name = '{1}'".format(message.text, message.from_user.id)
        cursor.execute(select_Query)
        connection.commit()
        
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL в save_topic_BD. Error = {0}". format(error))
        #print("Закрыто connection из Error. Value {0}".format(connection))
    finally:
        if connection:
            print("Соединение с PostgreSQL закрыто из save_topic_BD")
            bot.send_message( message.from_user.id , "Я сохранил имя топика")
            start_menu(message)
#--------------Старт меню---------------------

def start_menu(message):
    global back_part
    markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
    btn1 = types.KeyboardButton ("Расход воды")
    btn2 = types.KeyboardButton ("Расход электричества")
    btn3 = types.KeyboardButton ("Изменить имя топика")
    markup.add (btn1, btn2, btn3)
    back_part = 1
    bot.send_message( message.from_user.id ,"Выберите по какому типу ресурсов предоставить расход" ,reply_markup = markup)

def back(message):
    if ((message.text == "Назад" and Back_counter == 1) or (message.text == "Назад" and Back_counter == 2)):
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
        btn1 = types.KeyboardButton ("Расход воды")
        btn2 = types.KeyboardButton ("Расход электричества")
        markup.add (btn1, btn2)
        bot.reply_to(message, "Есть!" ,reply_markup = markup )

#--------------Всё что связано с водой--------

def consumption_water(message):
    global Back_counter
    if (message.text == "Расход воды" or Back_counter == 3):
        Back_counter = 0
        markup = types.ReplyKeyboardMarkup(row_width = 1, one_time_keyboard = True, resize_keyboard= True) 
        btn1 = types.KeyboardButton ("Расход воды за месяц")
        btn2 = types.KeyboardButton ("Расход воды за всё время")
        btn3 = types.KeyboardButton ("Внести показания счетчика")
        btn4 = types.KeyboardButton ("Назад")
        markup.add (btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Главное меню" ,reply_markup = markup )
        Back_counter = 1

def insert_data_water(message):
    if message.text == "Внести показания счетчика":
        msg = bot.reply_to( message , "Введите показания счетчика холодной воды")
        bot.register_next_step_handler(msg, insert_data_water_cold)

def insert_data_water_cold(message):
    try:
        check_bit = 0
        if (isfloat(message.text)):
            #connection = connection_BD
            cursor = connection.cursor()
            select_Query = "update dev_1 set data_cold = {0} where u_name = '{1}'".format(float(message.text), message.from_user.id)
            cursor.execute(select_Query)
            connection.commit()
            check_bit = 1 
        else:

            msg = bot.send_message( message.from_user.id , 'Неверный формат вводимого значения. Значение должно быть нецелым и вводится через точку. Попробуйте ещё раз')
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL из insert_data_water_cold. Error = {0}".format(error))
    finally:
        if check_bit:
            #cursor.close()
            #connection.close()
            msg_hot = bot.send_message (message.from_user.id , "Введите показания горячей воды")
            bot.register_next_step_handler(msg_hot, insert_data_water_hot)
            print("Соединение с PostgreSQL закрыто из insert_data_water_cold")
        else:
            bot.register_next_step_handler(msg, insert_data_water_cold)

def insert_data_water_hot(message):
    try:
        check_bit = 0
        global Back_counter
        if (isfloat(message.text)):
            #connection = connection_BD
            cursor = connection.cursor()
            select_Query = "update dev_1 set data_hot = '{0}' where u_name = '{1}'".format(float(message.text), message.from_user.id)
            cursor.execute(select_Query)
            connection.commit()
            check_bit = 1
        else:
            msg = bot.send_message( message.from_user.id , 'Неверный формат вводимого значения. Значение должно быть нецелым и вводится через точку. Попробуйте ещё раз')
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL из insert_data_water_hot. Error = {0}".format(error))
    finally:
        if check_bit:
            bot.send_message (message.from_user.id , "Сохранил показания")
            Back_counter = 3
            consumption_water(message)
            print("Соединение с PostgreSQL закрыто из insert_data_water_cold")
        else:
            bot.register_next_step_handler(msg, insert_data_water_hot)

#-----------------------------------------------------------------------
#---------------------Электричетсво-------------------------------------
#-----------------------------------------------------------------------

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

def consumption_electricity_month(message):
    if (message.text == "Расход электричества за месяц"):
        #print("Error1")
        data = get_data_from_BD()
        #print (data)
        bot.send_message (message.from_user.id, "Расход электричества - {0} кВт".format(data[2]))

#------------------Некоторые полезные функции---------------
def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

bot.infinity_polling()
