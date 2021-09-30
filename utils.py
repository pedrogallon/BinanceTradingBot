import logging
import urllib.request
import urllib.parse
from datetime import datetime
import schedule
import time
import sqlite3
from binance.client import Client
from binance.enums import *
from binance.exceptions import *


binance_client = {}
settings = {}


def get_time_string():
    return str(datetime.today())


def get_time_unix():
    return time.time()


def send_message(message):
    get_logger().info("CallMeBot - Sending message")
    urllib.request.urlopen("https://api.callmebot.com/whatsapp.php?apikey="
        + get_settings().get("callmebot_api_key") + "&phone=" + get_settings().get("callmebot_number")
        + "&text=" + urllib.parse.quote_plus(get_time_string() + "\n" + message))


def get_settings():
    global settings
    if settings == {}:
        settings = json.loads(open('settings.json').read())

    return settings


def get_binance_client():
    global binance_client
    if binance_client == {}:
        binance_client = Client(get_settings().get("binance_api_key"), get_settings().get("binance_api_secret"))

    return binance_client


def print_binance_balance():
    print('\n-- ACCOUNT BALANCE --')
    for b in get_binance_client().get_account().get('balances'):
        if float(b.get('free')) > 0:
            print(b.get('asset') + ": \t" + b.get('free'))


def schedule_every_minute(function, interval):
    get_logger().info("Scheduled function {} to run every {} minutes".format(function.__name__, interval))
    schedule.clear()
    schedule.every(interval).minutes.do(function)
    while True:
        schedule.run_pending()


def get_tickers():
    tickers = []
    for ticker in get_settings().get("tickers"):
        tickers.append(ticker.get("symbol"))
    return tickers


def get_db():
    db = sqlite3.connect('database/database.db')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM price_history")

    except:
        get_logger().info("Initializing database with initialize_db.sql")
        cursor.execute(open('database/initialize_db.sql').read())
        db.commit()

    finally:
        return db


def insert_db_price_history(time, symbol, price, delta):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO price_history (time, symbol, price, delta) VALUES (?, ?, ?, ?)", (time, symbol, price, delta))
    db.commit()


def send_market_order(type, ticker, amount):
    log = get_logger()
    message = "Sending market order: {} {} {}".format(type, amount, ticker )
    log.info(message)
    send_message(message)
    try:
        get_binance_client().create_order(
            symbol=ticker,
            side=type,
            type=ORDER_TYPE_MARKET,
            quantity=amount)
        log.info("Market order succesful")
    except:
        message = "Problem sending {} order of {} {}".format(type, amount, ticker)
        send_message(message)
        log.exception(message)


def get_logger():
    logging.basicConfig(format='%(asctime)-15s [%(levelname)s]\t- %(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler("logging.log"),
                            logging.StreamHandler()
                        ])

    return logging.getLogger()


def get_ticker(symbol):
    ticker = {}
    for ticker in get_settings().get("tickers"):
        if ticker.get('symbol') == symbol:
            ticker = ticker
    return ticker
