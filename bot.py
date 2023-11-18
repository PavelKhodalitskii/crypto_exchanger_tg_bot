import json
import telebot
from telebot import types
import random

from user import User
from database import DataAccessObject
from modules.news_scratch import get_news

token = ''

with open("../secret.txt", 'r') as file:
    token = file.readline().strip()
bot = telebot.TeleBot(token)
    
@bot.message_handler(commands=['start', 'Help', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(True, row_width=2)
    helper = types.KeyboardButton('Менеджер')
    wallet = types.KeyboardButton('Кошелёк')
    exchanger = types.KeyboardButton('Обменник')
    news = types.KeyboardButton('Новости')
    about_service = types.KeyboardButton('О сервисе')
    
    markup.add(helper, wallet, exchanger, about_service, news)
    bot.send_message(message.chat.id, '🚀Добро пожловать в крипто обменник!', reply_markup=markup)

    user_id = message.from_user.id
    user = User(str(user_id))

@bot.message_handler(content_types=['text'])
def command(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        user = User(str(user_id))

        if message.text == 'Новости':
            news_data = get_news()
            bot.send_message(message.chat.id, f"{news_data['news_date']} | {news_data['news_name']} | {news_data['news_text']} | {news_data['url']}",
                parse_mode='html')
        elif message.text == 'Менеджер':
            managers = ['https://t.me/AlexLand0']
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Менеджер', url=random.choice(managers)))
            bot.send_message(message.chat.id, 'Напишите менеджеру', reply_markup=markup)
        elif message.text == 'Кошелёк':

            markup = types.InlineKeyboardMarkup(row_width=2)
            fill_up_button = types.InlineKeyboardButton("⬆ Пополнить ", callback_data='Пополнить')
            withdraw_button = types.InlineKeyboardButton("⬇ Снять ", callback_data='Снять')
            markup.add(fill_up_button, withdraw_button)

            balance_data = user.get_balance_data()
            bot_message_balance = (
                f"💵 Баланс BTC: {balance_data['BTC']}\n💵 Баланс ETH: {balance_data['ETH']}")
            bot.send_message(message.chat.id, bot_message_balance, reply_markup=markup)
        elif message.text == 'О сервисе':
            bot.send_message(message.chat.id, 'О нас: ')
        elif message.text == 'Обменник':
            markup = types.InlineKeyboardMarkup(row_width=2)
            btc_to_eth = types.InlineKeyboardButton("BTC->ETH", callback_data='BTC-ETH')
            eth_to_btc = types.InlineKeyboardButton("ETH->BTC", callback_data='ETH-BTC')
            markup.add(btc_to_eth, eth_to_btc)
            bot.send_message(message.chat.id, 'Перевод', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'не понял команду')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Пополнить':
                markup = types.InlineKeyboardMarkup(row_width=2)
                btc_fillup = types.InlineKeyboardButton("BTC ", callback_data='BTC_fill_up')
                eth_fillup = types.InlineKeyboardButton("ETH ", callback_data='ETH_fill_up')
                markup.add(btc_fillup, eth_fillup)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Чтобы пополнить кошелек, Вам надо перевести Ваши стредства на многоразовый адрес который будет указан ниже\nПосле перевода и подтверждения 1 транзакции, Ваши средства будут отображаться у Вас в кошельке.",
                                    reply_markup=markup)
            elif call.data == 'Снять':
                markup = types.InlineKeyboardMarkup(row_width=2)
                btc_withdraw = types.InlineKeyboardButton("BTC ", callback_data='BTC_withdraw')
                eth_withdraw = types.InlineKeyboardButton("ETH ", callback_data='ETH_withdraw')
                markup.add(btc_withdraw, eth_withdraw)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Чтобы снять деньги, Вам надо ввести адрес кошелька на который будет выполнен перевод. \nПосле перевода и подтверждения 1 транзакции, Ваши средства будут отображаться у Вас в кошельке.",
                                    reply_markup=markup)
            elif call.data == 'BTC_fill_up':
                bot.send_message(chat_id=call.message.chat.id, text=f"Пополнение с помощью BTC:\n (Не менее 0,00000547 BTC)\n BTC Кошелек: {User(call.message.chat.id).get_btc_wallet_number()}")
            elif call.data == 'ETH_fill_up':
                bot.send_message(chat_id=call.message.chat.id, text=f"Пополнение с помощью ETH:\n (Не менее 0,00000547 ETH)\n ETH Кошелек: {User(call.message.chat.id).get_eth_wallet_number()}")
            elif call.data == 'BTC_withdraw':
                withdraw_to_btc_address = call.message.text
            elif call.data == 'ETH_withdraw':
                withdraw_to_eth_address = call.message.text
            elif call.data == 'BTC-ETH':
                bot.send_message(chat_id=call.message.chat.id, text=f"Переод из BTC в ETH. Введите сумму: ")
            elif call.data == 'ETH-BTC':
                bot.send_message(chat_id=call.message.chat.id, text=f"Переод из ETH в BTC. Введите сумму: ")
    except Exception as e:
        print(repr(e))

database = DataAccessObject()
bot.polling(none_stop=True)


# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         time.sleep(15)