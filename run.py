import pytz, datetime, time

from symbol_CLI import symbol_cli
from parameter_writer import parameter_writer
from support_resistance_detector import level_detector

eastern = pytz.timezone("US/Eastern")
now = datetime.datetime.now(eastern)
aftermarket_end_incoming = now.replace(hour=19, minute=45, second=0, microsecond=0) # 19:45 EDT / 00:45 BST


if __name__ == "main":
    symbols = symbol_cli()

    while True:
        now = datetime.datetime.now(eastern)

        if now >= aftermarket_end_incoming:
            levels_dict = level_detector(symbols)
            parameter_writer(levels_dict)
        else: 
            time.sleep(300) # 5min


