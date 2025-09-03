from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarRequest
from alpaca.data.timeframe import TimeFrame

import pytz, datetime

from dotenv import load_dotenv
import os

# ALPACA 15MIN TIMEFRAME BUG
    # REQUEST 5MIN BARS, WRITE AGGREGATOR...
    # will 3x the number of bars requested - for intra + 5d, 1,101 bars per symbol (max 9 symbols)

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

intraday_prices = {}
bar_data = {}
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

async def level_detector(symbols):
    for key in symbols:
        if key[-1].isdigit():
            lookback_days = int(key[-1])
            lookback_minutes = 705 + lookback_days*960

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



    # alpaca api request for s in symbols
        # 19:45 call, 11:45 + 16:00 (04:00-20:00, full day) * 5 = 91:45 (current day + last 5 days)
            # is there a way to only request relevant days per ticker...?
            # e.g. give option for days in CLI?
        # 15min per bar, 367 bars for intra + 5d, * ~20 symbols = 7,340 (MAX 27 symbols, 9,909)
            # single request limit = 10,000 bars
            # 20 requests/min
        # split requests into []s per days of historical data needed
            # results in: 1) way under 10k per request, 2) total ~6 requests

        # fetch 5, 4, 3, 2, 1, and 0 days back
        # 0 days means intraday only
        # all other ones means intraday + x days
            # use this to calculate lookback minutes in support_resistance_detector
            # e.g. 2 days = 11:45 (intra) + 16hr (full day) * 2 (day count) = 43.75hrs
    
    # append intraday_prices, bar_data
        # intraday = bar_data[-1]['close']?
        # calculate stdev per symbol

    # take bar_data df, append local_extrema_sd with?:
        # 1. local extrema of sliding window, 2. pivot points with strength score?, 3. reduce noise via fractals?, 4. calculate stdev

    # logic to find closest appropriate levels per symbol
        # append levels with upper level + stdev, lower level - stdev, rounded to 4sf
        # ...with the below format

    return levels


# desired output:
    #{
        #{"AAPL": [100.0, 95.0], "TSLA": [234.0, 223.0], ...},
        #"dollar_value": 4000.0
    #}


