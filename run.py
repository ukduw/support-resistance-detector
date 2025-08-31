import pytz, datetime, time

from symbol_CLI import symbol_cli
from parameter_writer import parameter_writer
from support_resistance_detector import LevelDetector

eastern = pytz.timezone("US/Eastern")
now = datetime.datetime.now(eastern)
aftermarket_end_incoming = now.replace(hour=19, minute=45, second=0, microsecond=0) # 19:45 EDT / 00:45 BST

ld = LevelDetector()
    # might change back... seems a lot more straightforward to call one function that does it all


if __name__ == "main":
    symbols = symbol_cli()

    while True:
        now = datetime.datetime.now(eastern)

        if now >= aftermarket_end_incoming:
            ld.fetch_candlestick_data(symbols)
            ld.find_local_extrema()
            levels_dict = ld.closest_extrema()
                # or, levels_dict = level_detector(symbols) - if changed back to one function...

            parameter_writer(levels_dict)
        else: 
            time.sleep(300) # 5min


