import telebot
from telebot import types
import csv 
import json
from decouple import config
from bs4 import BeautifulSoup
import requests
import lxml

bot = telebot.TeleBot(config('TOKEN'), parse_mode=None)

main_inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
USD = types.InlineKeyboardButton('USD', callback_data='usd')
EUR = types.InlineKeyboardButton('EUR', callback_data='eur')
RUB = types.InlineKeyboardButton('RUB', callback_data='rub')
KZT = types.InlineKeyboardButton('KZT', callback_data='kzt')
NBKR = types.InlineKeyboardButton('Курc валют НБКР', callback_data='nbkr')
main_inline_keyboard.add(USD, EUR, RUB, KZT, NBKR)

@bot.message_handler(commands=['start', 'help', 'Старт', 'старт', 'начать', 'начни', 'стартуй', 'стартовать', 'двигайся'])
def to_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Здравствуйте!")
    bot.send_message(chat_id, "Выберите валюту, пожалуйста!", reply_markup=main_inline_keyboard )

@bot.callback_query_handler(func=lambda call:True)
def obrabotka_callback(call):
    if call.data == 'usd':
        chat_id = call.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        a1 = types.KeyboardButton('Покупка USD')
        a2 = types.KeyboardButton('Продажа USD')
        income_keyboard.add(a1, a2)
        msg = bot.send_message(chat_id, 'Выберите процесс:', reply_markup=income_keyboard)
        bot.register_next_step_handler(msg, get_categori)
    elif call.data == 'eur':
        chat_id = call.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        a1 = types.KeyboardButton('Покупка EUR')
        a2 = types.KeyboardButton('Продажа EUR')
        income_keyboard.add(a1, a2)
        msg = bot.send_message(chat_id, 'Выберите процесс:', reply_markup=income_keyboard)
        bot.register_next_step_handler(msg, get_categori)
    elif call.data == 'rub':
        chat_id = call.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        a1 = types.KeyboardButton('Покупка RUB')
        a2 = types.KeyboardButton('Продажа RUB')
        income_keyboard.add(a1, a2)
        msg = bot.send_message(chat_id, 'Выберите процесс:', reply_markup=income_keyboard)
        bot.register_next_step_handler(msg, get_categori)
    elif call.data == 'kzt':
        chat_id = call.message.chat.id
        income_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        a1 = types.KeyboardButton('Покупка KZT')
        a2 = types.KeyboardButton('Продажа KZT')
        income_keyboard.add(a1, a2)
        msg = bot.send_message(chat_id, 'Выберите процесс:', reply_markup=income_keyboard)
        bot.register_next_step_handler(msg, get_categori)
    elif call.data == 'nbkr':
        chat_id = call.message.chat.id
        bot.send_message(chat_id, 'Курсы валют по статистике НБКР')
        with open("NBKR_kurs.json","rb") as file:
            f=file.read()
        bot.send_document(chat_id,f,"NBKR_kurs.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def get_categori(message):
    if message.text == 'Покупка USD':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_usd_buy)
    elif message.text == 'Продажа USD':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_usd_sell)
    elif message.text == 'Покупка EUR':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_eur_buy)
    elif message.text == 'Продажа EUR':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_eur_sell)
    elif message.text == 'Покупка RUB':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_rub_buy)
    elif message.text == 'Продажа RUB':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_rub_sell)
    elif message.text == 'Покупка KZT':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_kzt_buy)
    elif message.text == 'Продажа KZT':
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        k = types.KeyboardButton('Лучшая цена (узнать)?')
        k1 = types.KeyboardButton('Скачать все данные: Json')
        markup.add(k, k1)
        msg = bot.send_message(chat_id, 'Выберите нужное:', reply_markup=markup )
        bot.register_next_step_handler(msg, send_kzt_sell)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_usd_buy(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("USD_BUY.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"USD_BUY.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("USD_BUY.json", "rb") as file:
            data_usd_buy = json.loads(file.read())
            key_usd_buy = data_usd_buy["usd_buy"]
        bot.send_message(chat_id, f"Банк и курс: {key_usd_buy}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_usd_sell(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("USD_SELL.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"USD_SELL.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("USD_SELL.json", "rb") as file:
            data_usd_sell = json.loads(file.read())
            key_usd_sell = data_usd_sell["usd_sell"]
        bot.send_message(chat_id, f"Банк и курс: {key_usd_sell}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_eur_buy(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("EUR_BUY.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"EUR_BUY.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("EUR_BUY.json", "rb") as file:
            data_eur_buy = json.loads(file.read())
            key_eur_buy = data_eur_buy["eur_buy"]
        bot.send_message(chat_id, f"Банк и курс: {key_eur_buy}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_eur_sell(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("EUR_SELL.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"EUR_SELL.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("EUR_SELL.json", "rb") as file:
            data_eur_sell = json.loads(file.read())
            key_eur_sell = data_eur_sell["eur_sell"]
        bot.send_message(chat_id, f"Банк и курс: {key_eur_sell}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_rub_buy(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("RUB_BUY.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"RUB_BUY.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("RUB_BUY.json", "rb") as file:
            data_rub_buy = json.loads(file.read())
            key_rub_buy = data_rub_buy["rub_buy"]
        bot.send_message(chat_id, f"Банк и курс: {key_rub_buy}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_rub_sell(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("RUB_SELL.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"RUB_SELL.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("RUB_SELL.json", "rb") as file:
            data_rub_sell = json.loads(file.read())
            key_rub_sell = data_rub_sell["rub_sell"]
        bot.send_message(chat_id, f"Банк и курс: {key_rub_sell}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_kzt_buy(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("KZT_BUY.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"KZT_BUY.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("KZT_BUY.json", "rb") as file:
            data_kzt_buy = json.loads(file.read())
            key_kzt_buy = data_kzt_buy["kzt_buy"]
        bot.send_message(chat_id, f"Банк и курс: {key_kzt_buy}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_kzt_sell(message):
    if message.text == 'Скачать все данные: Json':
        chat_id = message.chat.id
        with open("KZT_SELL.json","rb") as file:
            f = file.read()
        bot.send_document(chat_id, f ,"KZT_SELL.json")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    elif message.text == 'Лучшая цена (узнать)?':
        chat_id = message.chat.id
        with open("KZT_SELL.json", "rb") as file:
            data_kzt_sell = json.loads(file.read())
            key_kzt_sell = data_kzt_sell["kzt_sell"]
        bot.send_message(chat_id, f"Банк и курс: {key_kzt_sell}")
        quit = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        q = types.KeyboardButton('Quit')
        quit.add(q)
        msg = bot.send_message(chat_id, 'Чтобы выйти нажмите Quit', reply_markup=quit)
        bot.register_next_step_handler(msg, send_dosvi)
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Вы в главном окне', reply_markup=main_inline_keyboard)

def send_dosvi(message):
    if message.text == 'Quit':
        chat_id = message.chat.id
        bot.send_message(chat_id, 'До свидания!')
    else:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Для продолжения наберите /start')



# PARSING PART
def get_html(url):
    r = requests.get(url)
    return r.text

def get_soup_NBKR(html):
    soup = BeautifulSoup(html, 'lxml')
    main_parsing_code_NBKR = soup.find('div', class_='rates-grid').find_all('div', class_='col-md-4')  
    for val in main_parsing_code_NBKR:
        try:
            valuta_name = val.find('h5').text.strip()
        except:
            print("None")
        try:
            kurs_valuta = val.find('div', class_='r-block__rate').text.strip()
        except:
            print("None")
        dict_NBKR_kurs = {'valuta': valuta_name, 'kurs': kurs_valuta}
        write_csv(dict_NBKR_kurs)

def write_csv(dict_NBKR_kurs):
    with open('NBKR_kurs.json', 'a') as file:
        json.dump(dict_NBKR_kurs, file)


def get_usd_buy(html):
    soup = BeautifulSoup(html, 'lxml')
    usd_buy = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')
    for soup_usd_buy in usd_buy:
        try:
            bank_usd_buy = soup_usd_buy.find('td').text.strip()
            usd_buy_kurs = soup_usd_buy.find('td',class_='td-rate').text.strip()
            print(bank_usd_buy, usd_buy_kurs)
        except:
            print("")
        dict_usd_buy = {'usd_buy': (bank_usd_buy, usd_buy_kurs)}
        write_usd_buy(dict_usd_buy)

def write_usd_buy(dict_usd_buy):
    with open('USD_BUY.json', 'w') as file:
        json.dump(dict_usd_buy, file)

def get_usd_sell(html):
    soup = BeautifulSoup(html, 'lxml')
    usd_sell = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')    
    for soup_usd_sell in usd_sell:
        try:
            bank_usd_sell = soup_usd_sell.find('td').text.strip()
            usd_sell_kurs = soup_usd_sell.find('td',class_='td-rate').text.strip()
            print(bank_usd_sell, usd_sell_kurs)
        except:
            print("")
        dict_usd_sell = {'usd_sell': (bank_usd_sell, usd_sell_kurs)}
        write_usd_sell(dict_usd_sell)

def write_usd_sell(dict_usd_sell):
    with open('USD_SELL.json', 'w') as file:
        json.dump(dict_usd_sell, file)

def get_eur_buy(html):
    soup = BeautifulSoup(html, 'lxml')
    eur_buy = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')
    for soup_eur_buy in eur_buy:
        try:
            bank_eur_buy = soup_eur_buy.find('td').text.strip()
            eur_buy_kurs = soup_eur_buy.find('td',class_='td-rate').text.strip()
            print(bank_eur_buy, eur_buy_kurs)
        except:
            print("")
        dict_eur_buy = {'eur_buy': (bank_eur_buy, eur_buy_kurs)}
        write_eur_buy(dict_eur_buy)

def write_eur_buy(dict_eur_buy):
    with open('EUR_BUY.json', 'w') as file:
        json.dump(dict_eur_buy, file)
        
def get_eur_sell(html):
    soup = BeautifulSoup(html, 'lxml')
    eur_sell = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')    
    for soup_eur_sell in eur_sell:
        try:
            bank_eur_sell = soup_eur_sell.find('td').text.strip()
            eur_sell_kurs = soup_eur_sell.find('td',class_='td-rate').text.strip()
            print(bank_eur_sell, eur_sell_kurs)
        except:
            print("")
        dict_eur_sell = {'eur_sell': (bank_eur_sell, eur_sell_kurs)}
        write_eur_sell(dict_eur_sell)

def write_eur_sell(dict_eur_sell):
    with open('EUR_SELL.json', 'w') as file:
        json.dump(dict_eur_sell, file)

def get_rub_buy(html):
    soup = BeautifulSoup(html, 'lxml')
    rub_buy = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')
    for soup_rub_buy in rub_buy:
        try:
            bank_rub_buy = soup_rub_buy.find('td').text.strip()
            rub_buy_kurs = soup_rub_buy.find('td',class_='td-rate').text.strip()
            print(bank_rub_buy, rub_buy_kurs)
        except:
            print("")
        dict_rub_buy = {'rub_buy': (bank_rub_buy, rub_buy_kurs)}
        write_rub_buy(dict_rub_buy)

def write_rub_buy(dict_rub_buy):
    with open('RUB_BUY.json', 'w') as file:
        json.dump(dict_rub_buy, file)
        
def get_rub_sell(html):
    soup = BeautifulSoup(html, 'lxml')
    rub_sell = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')    
    for soup_rub_sell in rub_sell:
        try:
            bank_rub_sell = soup_rub_sell.find('td').text.strip()
            rub_sell_kurs = soup_rub_sell.find('td',class_='td-rate').text.strip()
            print(bank_rub_sell, rub_sell_kurs)
        except:
            print("")
        dict_rub_sell = {'rub_sell': (bank_rub_sell, rub_sell_kurs)}
        write_rub_sell(dict_rub_sell)

def write_rub_sell(dict_rub_sell):
    with open('RUB_SELL.json', 'w') as file:
        json.dump(dict_rub_sell, file)

def get_kzt_buy(html):
    soup = BeautifulSoup(html, 'lxml')
    kzt_buy = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')
    for soup_kzt_buy in kzt_buy:
        try:
            bank_kzt_buy = soup_kzt_buy.find('td').text.strip()
            kzt_buy_kurs = soup_kzt_buy.find('td',class_='td-rate').text.strip()
            print(bank_kzt_buy, kzt_buy_kurs)
        except:
            print("")
        dict_kzt_buy = {'kzt_buy': (bank_kzt_buy, kzt_buy_kurs)}
        write_kzt_buy(dict_kzt_buy)

def write_kzt_buy(dict_kzt_buy):
    with open('KZT_BUY.json', 'w') as file:
        json.dump(dict_kzt_buy, file)
        
def get_kzt_sell(html):
    soup = BeautifulSoup(html, 'lxml')
    kzt_sell = soup.find('div', class_='col-md-9').find('tbody').find_all('tr')    
    for soup_kzt_sell in kzt_sell:
        try:
            bank_kzt_sell = soup_kzt_sell.find('td').text.strip()
            kzt_sell_kurs = soup_kzt_sell.find('td',class_='td-rate').text.strip()
            print(bank_kzt_sell, kzt_sell_kurs)
        except:
            print("")
        dict_kzt_sell = {'kzt_sell': (bank_kzt_sell, kzt_sell_kurs)}
        write_kzt_sell(dict_kzt_sell)

def write_kzt_sell(dict_kzt_sell):
    with open('KZT_SELL.json', 'w') as file:
        json.dump(dict_kzt_sell, file)

def main():
    url_NBKR = 'https://valuta.kg/rates/nbkr/'
    get_soup_NBKR(get_html(url_NBKR))
    url_usd_buy = 'https://valuta.kg/rates/buy/usd/84-40/'
    name = get_usd_buy(get_html(url_usd_buy))
    url_usd_sell = 'https://valuta.kg/rates/sell/usd/84-70/'
    get_usd_sell(get_html(url_usd_sell))
    url_eur_buy = 'https://valuta.kg/rates/buy/eur/101-80/'
    get_eur_buy(get_html(url_eur_buy))
    url_eur_sell = 'https://valuta.kg/rates/sell/eur/103-00/'
    get_eur_sell(get_html(url_eur_sell))
    url_rub_buy = 'https://valuta.kg/rates/buy/rub/1-142/'
    get_rub_buy(get_html(url_rub_buy))
    url_rub_sell = 'https://valuta.kg/rates/sell/rub/1-155/'
    get_rub_sell(get_html(url_rub_sell))
    url_kzt_buy = 'https://valuta.kg/rates/buy/kzt/0-1900/'
    get_kzt_buy(get_html(url_kzt_buy))
    url_kzt_sell = 'https://valuta.kg/rates/sell/kzt/0-2050/'
    get_kzt_sell(get_html(url_kzt_sell))
    
    bot.polling()

if __name__ == "__main__":
    main()
