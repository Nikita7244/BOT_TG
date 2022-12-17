import psycopg2
from telebot import *
from psycopg2 import Error
def get_data_from_BD():
    try:
        connection = psycopg2.connect (dbname = "Start", user = "postgres", password = "1", host = "localhost", port = "5432")
        cursor = connection.cursor()
        select_Query = "select data_hot, data_cold, data_light from test_py where id = 2"
        cursor.execute(select_Query)
        records = cursor.fetchone()
        return records
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто из get_data_from_BD")
def insert_name_to_BD(message):
    try:
        Name = message.text
        print("I'm alive")
        connection = psycopg2.connect (dbname = "Start", user = "postgres", password = "1", host = "localhost", port = "5432")
        cursor = connection.cursor()
        select_Query = "insert into login_py (name) values ('{0}')".format(Name)
        cursor.execute(select_Query)
        connection.commit()
        #id_from_table = search_nameid_in_login(Name)
        #insert_name_in_data(id_from_table[0], Name)
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL в insert_name_to_login")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто из insert_name_to_login")
def search_nameid_in_login(name):
    try:
        connection = psycopg2.connect (dbname = "Start", user = "postgres", password = "1", host = "localhost", port = "5432")
        cursor = connection.cursor()
        select_Query = "select name_id from login_py where name = '{0}'".format(name)
        cursor.execute(select_Query)
        records = cursor.fetchone()
        return records
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL из search_nameid_in_login")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто из search_nameid_in_login")
def insert_name_in_data(id, name):
    try:
        connection = psycopg2.connect (dbname = "Start", user = "postgres", password = "1", host = "localhost", port = "5432")
        cursor = connection.cursor()
        select_Query = "insert into test_py (id, name) values ({0}, '{1}')".format(id, name)
        cursor.execute(select_Query)
        connection.commit()
    except (Exception, Error) as error:
        print ("Ошибка при работе с SQL из insert_name_in_data")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто из insert_name_in_data")
if __name__ == "__main__":
    insert_name_to_BD()