from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarRequest
from alpaca.data.timeframe import TimeFrame

import pytz, datetime
import pandas as pd
import numpy as np

from decimal import Decimal, ROUND_UP, ROUND_DOWN

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

eastern = pytz.timezone("US/Eastern")

historical_client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


bar_data = {}
intraday_prices = {}

bar_data_15min = {}
standard_dev = {}
local_extrema = {}

closest_levels_up = {}
closest_levels_down = {}

levels = {}
output = {}
    # level strength score could be used for: 1. take-profit logic, 2. risk-off, 3. planning bigger plays


# symbols:      (example: symbol_list3 skipped; empty day)
    # {
    # "symbol_list5": ["AAPL", "TSLA", ...], 
    # "symbol_list4": ["ABC, BBBY, ..."],
    # "symbol_list2": ["GME", "MEME"...],
    # "symbol_list1": ["XYZ", ...],
    # "symbol_list0": ["BABA", "GABA", "BAGA", "GAGA", ...],
    # "dollar_value": 4000.0
    # }

# NOTE: 5min bars = 3x the bar requests - intra + 5d = 1,101 bars PER SYMBOL
    # symbol_list5 MAX 9 SYMBOLS

def level_detector(symbols):
    for key in symbols:
        if key[-1].isdigit():
            lookback_days = int(key[-1])
            lookback_minutes = 705 + lookback_days*960      # 705 - 4,800min

            now = datetime.datetime.now(eastern)
            start_time = now - datetime.timedelta(minutes=lookback_minutes)

            request_params = StockBarRequest(
                symbol_or_symbols=symbols[key],     # this ALWAYS returns multi-index df, even if list only contains 1 symbol
                timeframe=TimeFrame(5, TimeFrame.Minute),
                start=start_time,
                end=now,
                adjustment="raw",
                feed="sip"
            )

            bars = historical_client.get_stock_bars(request_params).df
            for symbol in bars.index.levels[0]:
                df = bars.xs(symbol, level=0).sort_index()
                bar_data[symbol].append(df)
                intraday_prices[symbol].append(df["close"].iloc[-1])

        else:
            dollar_value = symbols[key]

    for symbol in bar_data:
        for i in range(0, len(bar_data), 3):
            three_bar_window = bar_data[symbol][i:i+3]

            aggregated = {
                "open": three_bar_window[0].open,
                "high": max(bar.high for bar in three_bar_window),
                "low": min(bar.low for bar in three_bar_window),
                "close": three_bar_window[-1].close,
                "volume": sum(bar.volume for bar in three_bar_window)
            }

            bar_data_15min[symbol].append(aggregated) # convert to df when needed



    # calculate stdev per symbol
    # levels should have stdev bounds - i.e. candles shouldn't have to bounce off a price perfectly to contribute to a level's count
    # if so, using the upper and lower bound of 2 levels for entry/exit will increase risk %
        # remember to account for upper and lower bound for risk %
    # level +- stdev is the variable that needs to be evaluated with the below logic
        # not just single price point, but a small range
        # after determining levels, sort, iterate through, removing those that are within another's stdev
    # these represent the same level
    # which one to get rid of? the one that's been touched less recently? or less total touches?
        # add removed level's score to the one that replaces it


    # price zones using below +- 1 stdev (daily, per bar...?)
    # take bar_data df, append local_extrema_sd with?:
        # 1. local extrema of sliding window
            # local extrema over a sliding window of candlesticks
            # in other words, price points where price previously reversed
        # 2. pivot points with strength score?
            # count pivot candles at price points (+ bound%)
            # can score levels by number of pivot candles
            # pivot candle = higher/lower than previous/neighboring candles
        # 3. reduce noise via fractals?
            # essentially candle pattern: (green vs red) 1. ggg-rr, 2. rrr-gg
            # 1. reversal on hitting resistance, 2. reversal on hitting support
    # CONSIDER ONLY APPENDING LEVELS THAT ARE WITHIN 10-15% OF THE INTRADAY


    # local_extrema format:
        #{
        # "symbol1": {"level1": strength (int), "level2": strength, ...},
        # "symbol2": {...}
        #}
    for symbol in local_extrema:
        for level in local_extrema[symbol]:
            if float(level) > intraday_prices[symbol] and symbol[level] > 1:
                percent_diff = (float(level) + standard_dev[symbol] - intraday_prices[symbol]) / float(level) * 100
                if 5 <= percent_diff < 11:
                    closest_levels_up[symbol].append(float(level) + standard_dev[symbol])
            if float(level) < intraday_prices[symbol] and symbol[level] > 1:
                percent_diff2 = (float(level) - standard_dev[symbol] - intraday_prices[symbol]) / float(level) * 100
                if -9.9 <= percent_diff2 <= -5:
                    closest_levels_down[symbol].append(float(level) - standard_dev[symbol])

    for symbol in closest_levels_up:
        upper = min(closest_levels_up[symbol], intraday_prices[symbol]*1.05) + standard_dev[symbol]
        upper_rounded = float(Decimal(str(upper)).quantize(Decimal("0.01"), rounding=ROUND_UP)) if upper >= 1.00 else float(Decimal(str(upper)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
    for symbol in closest_levels_down:
        lower = max(closest_levels_down[symbol], upper_rounded*0.95) - standard_dev[symbol]
        lower_rounded = float(Decimal(str(lower)).quantize(Decimal("0.01"), rounding=ROUND_DOWN)) if lower >= 1.00 else float(Decimal(str(lower)).quantize(Decimal("0.0001"), rounding=ROUND_DOWN))
        levels[symbol] = [upper_rounded, lower_rounded]

    for symbol in levels:
        if len(levels[symbol]) < 2:
            levels.pop(symbol)

    output.append(levels)
    output["dollar_value"] = dollar_value
    
    return output


# desired output:
    #{
        #{"AAPL": [100.0, 95.0], "TSLA": [234.0, 223.0], ...},
        #"dollar_value": 4000.0
    #}


