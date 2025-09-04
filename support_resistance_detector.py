from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarRequest
from alpaca.data.timeframe import TimeFrame

import pytz, datetime
import pandas as pd
import numpy as np

from dotenv import load_dotenv
import os


# determine support/resistance levels - probably need to increase sensitivity for granular/weak levels
# levels should have x% bounds - i.e. candles shouldn't have to bounce off a price perfectly to contribute to a level's count
    # if so, using the upper and lower bound of 2 levels for entry/exit will increase risk %
    # level * bound% is the variable that needs to be evaluated with the below logic
# or, use average true range or standard deviation on top of these levels
# not just single price point, but a small range
    # again, remember to account for upper and lower bound for risk %
# after determining levels, sort, iterate through, removing those that are within another's stdev
    # these represent the same level
    # which one to get rid of? the one that's from being touched less recently?

# gist:
    # pivot points (most common method):
        # count pivot candles at price points (+ bound%)
        # can score levels by number of pivot candles
        # pivot candle = higher/lower than previous/neighboring candles
    # local maxima/minima:
        # local extrema over a sliding window of candlesticks
        # in other words, price points where price previously reversed
# remove noise via fractals?
    # essentially candle pattern: (green vs red) 1. ggg-rr, 2. rrr-gg
    # 1. reversal on hitting resistance, 2. reversal on hitting support


# need logic to determine:
    # levels closest to 5% of current price, within 10%
        # what if equidistant to 5%? e.g. 3 vs 7, 1 vs 9
    # just realized lower level should be 5-10% lower than the upper level used, not the intraday
    # if excessively close to current price, default to next closest level
    # if no upper in 5-10% range, default to <5 or >10?
    # if no lower in 5-10% range, just default to intraday??
# round to 4 significant figures

# build dict of entry/exit parameters per symbol
# return dict (to use in parameter_writer)

load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

bar_data = {}
intraday_prices = {}

bar_data_15min = {}
standard_dev = {}
local_extrema_sd = {}

levels = {}
    # level strength score could be used for: 1. take-profit logic, 2. risk-off, 3. planning bigger plays


eastern = pytz.timezone("US/Eastern")

historical_client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


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

async def level_detector(symbols):
    for key in symbols:
        if key[-1].isdigit():
            lookback_days = int(key[-1])
            lookback_minutes = 705 + lookback_days*960      # 705 - 4,800min

            now = datetime.datetime.now(eastern)
            start_time = now - datetime.timedelta(minutes=lookback_minutes)

            request_params = StockBarRequest(
                symbol_or_symbols=symbols[key], 
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

    # price zones using below +- 1 stdev (daily, per bar...?)
    # take bar_data df, append local_extrema_sd with?:
        # 1. local extrema of sliding window
        # 2. pivot points with strength score?
        # 3. reduce noise via fractals?
        # 4. calculate stdev

    # logic to find closest appropriate levels per symbol
        # append levels with upper level + stdev, lower level - stdev, rounded to 4sf
        # ...with the below format

    levels["dollar_value"] = dollar_value
    
    return levels


# desired output:
    #{
        #{"AAPL": [100.0, 95.0], "TSLA": [234.0, 223.0], ...},
        #"dollar_value": 4000.0
    #}


