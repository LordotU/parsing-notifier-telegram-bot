import csv
import html5lib
import logging
import os
import requests
import sys
import telegram

from bs4 import BeautifulSoup
from parser import get_message

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

if TELEGRAM_API_TOKEN is None:
    logging.critical('TELEGRAM_API_TOKEN is required!')
    sys.exit()

TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

if TELEGRAM_CHAT_ID is None:
    logging.critical('TELEGRAM_CHAT_ID is required!')
    sys.exit()

bot = telegram.Bot(TELEGRAM_API_TOKEN)

csv_file = open('urls.csv', mode='r')
csv_reader = csv.DictReader(csv_file, delimiter=';')

for row in csv_reader:
    response = requests.get(row['url'])
    soup = BeautifulSoup(response.content, 'html5lib')
    message = get_message(row, soup)

    logging.debug(message)

    bot.send_message(chat_id=TELEGRAM_CHAT_ID,
                     text=message,
                     parse_mode=telegram.ParseMode.MARKDOWN)
