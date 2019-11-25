# Parsing Notifier — Telegram Bot

[![License](https://img.shields.io/badge/License-Unlicense-000000.svg)](https://unlicense.org/)

## Description

🤖 This bot is needed to parse the list of web pages and send messages with the parsing results.

## Usage

You may run your own copy of this bot with cron and Docker.

For example, this job will perform parsing and message sending every 12 hours:

```bash
0 */12 * * * docker run --rm -dti -e TELEGRAM_API_TOKEN=<Telegram API Token> -e TELEGRAM_CHAT_ID=<Telegram Chat ID> -v <Path to parser.py file>:/app/parser.py -v <Path to urls.csv file>:/app/urls.csv --name parsing-notifier-telegram-bot lordotu/parsing-notifier-telegram-bot >/dev/null 2>&1
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
    price_node = soup.find('span', class_='current-price')

    if price_node is None:
        return '*{0}*\n\n_Price was not found at:_\n\n{1}'.format(row['title'], row['url'])

    price_value = price_node.get_text()
    message = '*{0}*\n\n_{1}_'.format(row['title'], price_value)

    return message
```

_urls.csv_ file must contain one required field — `url`.

But, for instance, you may add any other additional fields:

```csv
url;title
https://www.tui.fi/search-flightonly-web/api/flightonly/searchresult?sort=rank&ep=2&market=fi&language=fi&departurecode=HEL&arrivalcode=TFS&durations=6%2C7%2C8%2C9&date=2019-11-26&ages=1%3B;26th of November
https://www.tui.fi/search-flightonly-web/api/flightonly/searchresult/?departurecode=HEL&arrivalcode=TFS&date=2019-11-30&ages=1%3B&durations=8&force=true&market=fi&language=fi;30th of November
```
