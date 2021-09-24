# -*- coding: utf-8 -*-

import utils

settings = utils.get_settings()
client = utils.get_binance_client()

currentPrices = client.get_all_tickers()
oldPrices = currentPrices

utils.print_binance_balance()


def check_prices():
    print('\n-- CHECKING PRICES --')
    global oldPrices
    global currentPrices
    currentPrices = client.get_all_tickers()

    tickers = []
    for ticker in settings.get("tickers"):
        tickers.append(ticker.get("symbol"))
    print(tickers)

    for current, old in zip(currentPrices, oldPrices):

        if current.get('symbol') in tickers:
            delta_percent = (float(current.get('price')) - float(old.get('price'))) / float(old.get('price')) * 100

            percent_margin = 0.0
            for ticker in settings.get("tickers"):
                if ticker.get('symbol') == current.get('symbol'):
                    percent_margin = ticker.get("percent_margin")

            print(current.get('symbol') + ":\t" + "%.5f" % delta_percent + ("\t - Variação acima de " + str(percent_margin) if delta_percent > percent_margin else ""))

            if delta_percent > percent_margin:
                utils.send_message(current.get('symbol') + " teve variação de " + str(delta_percent))

    oldPrices = currentPrices


utils.schedule_every_minute(check_prices, 2)

