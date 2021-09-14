# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:20:40 2021

@author: Gallon-PC
"""

from binance.client import Client
from threading import Timer
import json

settingsFile = open('settings.json').read()
settings = json.loads(settingsFile)

#settings = json.loads(settingsFile)

#print(settings.get("api_key"))

# API: https://python-binance.readthedocs.io/en/latest/account.html

#MEUS_ATIVOS = ['BTCUSDT','ETHUSDT','LTCUSDT','ADAUSDT','SOLUSDT']

###
# client = Client(api_key, api_secret)
client = Client(settings.get("api_key"), settings.get("api_secret"))

res = client.get_account()
#print(res.get('balances'))

print('-- ACCOUNT BALANCE --')
for b in res.get('balances'):
    if float(b.get('free'))> 0:
        print(b.get('asset')+": "+b.get('free'))

''
currentPrices = client.get_all_tickers()
oldPrices = currentPrices

def checkPrices():
    print('\n-- CHECKING PRICES --')
    global currentPrices
    global oldPrices
    currentPrices = client.get_all_tickers()
    for current, old in zip(currentPrices,oldPrices) :
        if current.get('symbol') in settings.get("tickers"):
            print(current.get('symbol'))
            increasePercent = (float(current.get('price'))- float(old.get('price'))) / float(old.get('price')) * 100
            print(increasePercent)
            
    
    oldPrices = currentPrices
    t = Timer(10.0, checkPrices)
    t.start()
        
checkPrices()