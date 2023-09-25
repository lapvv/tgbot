from json import JSONDecodeError
import telebot
from telebot.types import Message
import json
import requests
from datetime import datetime
# from bot_token import token
from envparse import Env
# from "https://www.cbr-xml-daily.ru/money.js" import money

from bot_request_service import TelegramClient

TOKEN = Env().str("TOKEN")
ADMIN_CHAT_ID = Env().str("ADMIN_CHAT_ID")
base_url = "https://https://api.telegram.org/"


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super(self.__class__, self).__init__(*args, **kwargs)
        self.telegram_client = telegram_client


telegram_client = TelegramClient(token=TOKEN, base_url=base_url)
bot = MyBot(token=TOKEN, telegram_client=telegram_client)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = telebot.types.KeyboardButton('Как дела?')
item2 = telebot.types.KeyboardButton('Курс валют EUR/RUB на сегодня')
item3 = telebot.types.KeyboardButton('Курс валют USD/RUB на сегодня')
markup.add(item1, item2, item3)


@bot.message_handler(commands=["start"])
def start(message: Message):
    with open("users.json", "r") as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}

    with open("users.json", "w") as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

    bot.reply_to(message=message, text=str(f"Вы зарегистрированы {username}. "
                                           f"Ваш user_id {user_id}."))
    bot.send_message(message.chat.id, 'Выберите команду из меню ниже:', reply_markup=markup)


# @bot.message_handler(commands=["Как дела?"])
# def report_request(message: Message):
#     bot.reply_to(message, text="Привет. Как дела?")
#     bot.register_next_step_handler(message, handle_response)

@bot.message_handler(content_types=['text'])
def report_request(message: Message):
    if message.chat.type == 'private':
        if message.text == "Как дела?":
            bot.send_message(message.chat.id, "Привет. Как дела?")
            bot.register_next_step_handler(message, handle_response)
        elif message.text == "Курс валют EUR/RUB на сегодня":
            rate = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
            # rate_obj = json.dumps(rate)
            # rate_str = json.loads(rate_obj)
            rate_eur = rate['Valute']['EUR']['Value']
            bot.send_message(message.chat.id, f"курс Евро к Рублю на {datetime.now():%Y-%m-%d}: {rate_eur}")
            bot.send_message(message.chat.id, 'Выберите команду из меню ниже:', reply_markup=markup)
        elif message.text == "Курс валют USD/RUB на сегодня":
            rate = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
            rate_usd = rate['Valute']['USD']['Value']
            bot.send_message(message.chat.id, f"курс Доллара США к Рублю на {datetime.now():%Y-%m-%d}: {rate_usd}")
            bot.send_message(message.chat.id, 'Выберите команду из меню ниже:', reply_markup=markup)


def handle_response(message: Message):
    bot.reply_to(message, "Спасибо что поделился")
    bot.send_message(message.chat.id, 'Выберите команду из меню ниже:', reply_markup=markup)


def create_err_message(err: Exception) -> str:
    return f"{datetime.now()}:::{err.__class__}:::{err}"


while True:
    try:
        bot.polling()
    except JSONDecodeError as err:
        bot.telegram_client.post(method="sendMessage", params={"text": create_err_message(err), "chat_id": ADMIN_CHAT_ID})
        # requests.post(f"https://api.telegram.org/bot{TOKEN}"
        #               f"/sendMessage?chat_id={}&text=)
