import json
import urllib.request
import urllib.parse
from datetime import datetime
import schedule
import time
from binance.client import Client


def send_message(message):

    print("-- CallMeBot - Mensagem Enviada -"+str(datetime.today()))
    urllib.request.urlopen("https://api.callmebot.com/whatsapp.php?apikey="
        + get_settings().get("callmebot_api_key") + "&phone=" + get_settings().get("callmebot_number")
        + "&text=" + urllib.parse.quote_plus(message))


def get_settings():
    return json.loads(open('settings.json').read())


def get_binance_client():
    settings = get_settings()
    return Client(settings.get("binance_api_key"), settings.get("binance_api_secret"))


def print_binance_balance():
    print('\n-- ACCOUNT BALANCE --')
    for b in get_binance_client().get_account().get('balances'):
        if float(b.get('free')) > 0:
            print(b.get('asset') + ": \t" + b.get('free'))


def schedule_every_minute(function, interval):
    schedule.clear()
    schedule.every(interval).minutes.do(function)
    while True:
        schedule.run_pending()
        time.sleep(1)
