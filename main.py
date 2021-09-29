# -*- coding: utf-8 -*-

import utils


log = utils.get_logger()
log.info("--APPLICATION STARTUP--")

settings = utils.get_settings()
client = utils.get_binance_client()
tickers = utils.get_tickers()

currentPrices = client.get_all_tickers()
oldPrices = currentPrices

utils.print_binance_balance()

last_order = "BUY"


def check_prices():
    log.info("check_prices running")
    print("\n-- PRICE CHECK DELTA --")
    global oldPrices
    global currentPrices
    global last_order
    currentPrices = client.get_all_tickers()

    for current, old in zip(currentPrices, oldPrices):

        if current.get('symbol') in tickers:
            delta_percent = (float(current.get('price')) - float(old.get('price'))) / float(old.get('price')) * 100

            ticker = utils.get_ticker(current.get('symbol'))

            print(current.get('symbol') + ":\t" + "%.5f" % delta_percent + ("\t - Variação acima de "
                + str(ticker.get('percent_margin')) if abs(delta_percent) > ticker.get('percent_margin') else ""))

            if (abs(delta_percent) > ticker.get('percent_margin')) and current.get('symbol') == 'AXSUSDT':
                if last_order == "BUY" and delta_percent < 0:
                    utils.send_market_order("SELL", ticker.get('symbol'), ticker.get('amount'))
                    last_order = "SELL"
                elif last_order == "SELL" and delta_percent > 0:
                    utils.send_market_order("BUY", ticker.get('symbol'), ticker.get('amount'))
                    last_order = "BUY"

            utils.insert_db_price_history(utils.get_time_unix(), current.get('symbol'), float(current.get('price')), delta_percent)

    oldPrices = currentPrices


utils.schedule_every_minute(check_prices, 1)




