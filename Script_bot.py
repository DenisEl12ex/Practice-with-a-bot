import requests
from datetime import datetime
import telebot
from auth_data import token


def get_data():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json() # в переменной будет лежать результат работы метода requests. используем метод json
    #print(response)

# достаем цену продажи
    sell_price = response["btc_usd"]["sell"] # получаем доступ к значениям ключей btc_usd и sell
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}") # вывод времени в удобном формате и новой строке стоимость валюты

# функция для бота с параметром "токен"
def telegram_bot(token):
    bot = telebot.TeleBot(token)

# декоратор + ф-ция для приветствия пользователя
    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend! Write the 'price' to find out the cost of BTC!")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn...Something was wrong..."
                )
        else:
            bot.send_message(message.chat.id, "Whaaaaat??? Check the command dude!")

    bot.polling()


if __name__ == '__main__':
    #get_data()
    telegram_bot(token)