# -*- coding: utf-8 -*-


from binance.enums import *
from binance.client import Client
from binance.exceptions import *
import json

settingsFile = open('settings.json').read()
settings = json.loads(settingsFile)

client = Client(settings.get("api_key"), settings.get("api_secret"))
account = client.get_account()

print('-- ACCOUNT BALANCE --')
for b in account.get('balances'):
    if float(b.get('free')) > 0:
        print(b.get('asset') + ": " + b.get('free'))

info = client.get_symbol_info('AXSUSDT')
print(info)

print('\n-- ORDER STARTED --')
try:
    order = client.create_test_order(
        symbol='AXSUSDT',
        side=SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=0.99)
except BinanceAPIException as e:
    print(e)
except BinanceOrderException as e:
    print(e)
print('-- ORDER COMPLETED --\n')

account = client.get_account()
print('-- ACCOUNT BALANCE --')
for b in account.get('balances'):
    if float(b.get('free')) > 0:
        print(b.get('asset') + ": " + b.get('free'))
