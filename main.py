# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:20:40 2021

@author: Gallon-PC
"""

import schedule
import time
from binance.client import Client
import json

settingsFile = open('settings.json').read()
settings = json.loads(settingsFile)

client = Client(settings.get("api_key"), settings.get("api_secret"))
res = client.get_account()

print('-- ACCOUNT BALANCE --')
for b in res.get('balances'):
    if float(b.get('free')) > 0:
        print(b.get('asset') + ": " + b.get('free'))

currentPrices = client.get_all_tickers()
oldPrices = currentPrices


def check_prices():
    print('\n-- CHECKING PRICES --')
    global currentPrices
    global oldPrices
    currentPrices = client.get_all_tickers()
    for current, old in zip(currentPrices, oldPrices):
        if current.get('symbol') in settings.get("tickers"):
            print(current.get('symbol'))
            increase_percent = (float(current.get('price')) - float(old.get('price'))) / float(old.get('price')) * 100
            print(increase_percent)
    oldPrices = currentPrices


schedule.clear()
schedule.every(10).seconds.do(check_prices)
while True:
    schedule.run_pending()
    time.sleep(1)
