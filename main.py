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


def check_prices():
    log.info("check_prices running")
    print("\n-- PRICE CHECK DELTA --")
    global oldPrices
    global currentPrices
    currentPrices = client.get_all_tickers()

    for current, old in zip(currentPrices, oldPrices):

        if current.get('symbol') in tickers:
            delta_percent = (float(current.get('price')) - float(old.get('price'))) / float(old.get('price')) * 100

            percent_margin = 0.0
            for ticker in settings.get("tickers"):
                if ticker.get('symbol') == current.get('symbol'):
                    percent_margin = ticker.get("percent_margin")

            print(current.get('symbol') + ":\t" + "%.5f" % delta_percent + ("\t - Variação acima de " + str(percent_margin) if abs(delta_percent) > percent_margin else ""))

            if abs(delta_percent) > percent_margin:
                utils.send_message(current.get('symbol') + " teve variação de " + str(delta_percent))

            utils.insert_db_price_history(utils.get_time_unix(), current.get('symbol'), float(current.get('price')), delta_percent)

    oldPrices = currentPrices


utils.schedule_every_minute(check_prices, 1)




