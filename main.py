from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
import os
from keyboards import *
import requests

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Welcome to Weather Bot!", reply_markup=generate_buttons())


@bot.message_handler(regexp="Weather 🌥️")
def ask_city(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Send your city name")
    bot.register_next_step_handler(msg, input_city)


def input_city(message: Message):
    chat_id = message.chat.id
    text = message.text.capitalize()
    bot.send_message(chat_id, f"Name of city: {text}")

    KEY = os.getenv('KEY')
    params = {
        'appid': KEY,
        'units': 'metric',
        'lang': 'en',
        'q': text,
    }
    data = requests.get("https://api.openweathermap.org/data/2.5/weather?", params=params).json()
    # print(data)
    try:
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        answer = (f"In {text} city {temp} c⁰\n"
                  f"Wind Speed: {wind_speed} km/h\n"
                  f"Descption: {description}")
        bot.send_message(chat_id, answer)
        ask_again(message)
    except Exception as e:
        msg = bot.send_message(chat_id, "Something went wrong.\n"
                                  "Enter again")
        bot.register_next_step_handler(msg, input_city)


def ask_again(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Push the button to ask again 👇🏿",
                     reply_markup=generate_buttons())

bot.polling(none_stop=True)