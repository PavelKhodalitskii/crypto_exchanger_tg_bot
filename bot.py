import telebot
from telebot import types
import random
import requests
from bs4 import BeautifulSoup

from user import User

token = ''
with open("../secret.txt", 'r') as file:
    token = file.readline().strip()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'Help', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(True, row_width=2)
    helper = types.KeyboardButton('/Helper')
    wallet = types.KeyboardButton('/Wallet')
    exchanger = types.KeyboardButton('/Exchanger')
    newss = types.KeyboardButton('/News')
    about_service = types.KeyboardButton('/About the service')
    markup.add(helper, wallet, exchanger, about_service, newss)
    bot.send_message(message.chat.id, 'Команды', reply_markup=markup)

    user_id = message.from_user.id
    user = User(str(user_id))
    print(user.get_balance())


@bot.message_handler(commands=['Helper', 'helper', 'менеджер'])
def helpers(message):
    managers = ['https://t.me/AlexLand0, https://t.me/AlexLand01, https://t.me/AlexLand02']
    markap = types.InlineKeyboardMarkup()
    markap.add(types.InlineKeyboardButton('Helper', url=random.choice(managers)))
    bot.send_message(message.chat.id, 'Helper12', reply_markup=markap)


@bot.message_handler(commands=['News'])
def news(message):

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    URL = "https://bits.media/news/"
    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    newsss = soup.find_all("div", class_="news-item")
    for new in newsss:

        news_date = new.find("span", class_="news-date").text.strip()
        news_name = new.find("a", class_="news-name").text.strip()
        news_text = new.find("div", class_="news-text").text.strip()
        url = f'https://bits.media{new.find("a", class_="news-name", href=True)["href"].strip()}'
        bot.send_message(message.chat.id, f"{news_date} | {news_name} | {news_text} | {url}", parse_mode='html')


bot.polling(none_stop=True)