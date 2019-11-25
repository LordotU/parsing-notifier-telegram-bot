import aiohttp
import asyncio

import csv
import html5lib
import logging
import os
import sys

from aiogram import Bot, types
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

bot = Bot(TELEGRAM_API_TOKEN)


async def send_message(row):
    async with aiohttp.ClientSession() as session:
        async with session.get(row['url']) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html5lib')
            message = get_message(row, soup)

            logging.debug(message)

            await bot.send_message(chat_id=TELEGRAM_CHAT_ID,
                                   text=message,
                                   parse_mode=types.ParseMode.MARKDOWN)


async def main():
    with open('urls.csv', mode='r') as csv_file:
        messages = [send_message(row)
                    for row in csv.DictReader(csv_file, delimiter=';')]

        await asyncio.gather(*messages)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
