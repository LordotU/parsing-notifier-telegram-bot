# Parsing Notifier — Telegram Bot

[![License](https://img.shields.io/badge/License-Unlicense-000000.svg)](https://unlicense.org/)

## Description

🤖 This bot is needed to parse the list of web pages and send messages with the parsing results.

## Usage

You may run your own copy of this bot with Docker:

```bash
docker pull lordotu/parsing-notifier-telegram-bot

docker run -dti \
  -e TELEGRAM_API_TOKEN=<Telegram API Token> \
  -e TELEGRAM_CHAT_ID=<Telegram Chat ID> \
  -v <Path to parser.py file>:/app/parser.py \
  -v <Path to urls.csv file>:/app/urls.csv \
  --name parsing-notifier-telegram-bot \
  lordotu/parsing-notifier-telegram-bot
```

But before, you should register your bot via **BotFather** https://t.me/BotFather, start using it and get Chat ID via this address `https://api.telegram.org/bot<Telegram API TOKEN>/getUpdates`

## Configuring

_parser.py_ file must implement only one function — `get_message(row, soup)`.

For example:

```python
def get_message(row, soup):
    """
    Returns the Markdown formatted message

    Args:
        row (OrderedDict): A dictionary representation of urls.csv file row.
        soup (BeautifulSoup): A Beautiful Soup web page representation.

    Returns:
        message (str): Markdown formatted message
    """
    current_price = soup.find('span', class_='current-price').get_text()
    message = '*{0}*\n\n_{1}_'.format(row['title'], current_price)
    return message
```

_urls.csv_ file must contain one required field — `url`.

But, for instance, you may add any other additional fields:

```csv
url;title
https://www.tui.fi/search-flightonly-web/api/flightonly/searchresult?sort=rank&ep=2&market=fi&language=fi&departurecode=HEL&arrivalcode=TFS&durations=6%2C7%2C8%2C9&date=2019-11-26&ages=1%3B;26th of November
https://www.tui.fi/search-flightonly-web/api/flightonly/searchresult/?departurecode=HEL&arrivalcode=TFS&date=2019-11-30&ages=1%3B&durations=8&force=true&market=fi&language=fi;30th of November
```
