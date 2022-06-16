import datetime
import telebot
import os

import threading


bot = telebot.TeleBot("5545318839:AAEUyTj6OSwaAI-B870xvn3ueDPYbCBZAk8", parse_mode=None)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    os.environ["CHAT_ID"] = str(message.chat.id)
    bot.reply_to(message, "Bot is active")


def send_message(order_number: int, order_date: datetime.date):
    bot.send_message(
        int(os.getenv("CHAT_ID")),
        f"Срок поставки заказ №{order_number} истек. Последняя дата поставки - {order_date}",
    )


my_thread = threading.Thread(target=lambda: bot.polling())
print("thread is active")
my_thread.start()
