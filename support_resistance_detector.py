# alpaca api call for 5(? less? 6?) days of historical data
    # high, low, open, close, indicators (standard deviation...)
    # decide between 5min and 15min data

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



# symbols:
    #{"symbol_list": ["AAPL", "TSLA", ...], "dollar_value": 4000.0}

class LevelDetector:
    def __init__(self):
        self.intraday_prices = {}
        self.bar_data = {}
        
        self.local_extrema = {}
        self.symbol_levels = {}

    def fetch_candlestick_data(self, symbols):
        return # request for s in symbols, append self.intraday_prices + self.bar_data
    
    def find_local_extrema(self, df, window=10):
        return # take df, append self.local_extrema with extrema of each sliding window per symbol (remember to use a tolerance %)
    
    def closest_extrema(self):
        return # logic to find closest appropriate levels (+ bound%) to intraday price per symbol, append self.symbol_levels with the below format


# desired output:
    #{
        #{"AAPL": [100.0, 95.0], "TSLA": [234.0, 223.0], ...},
        #"dollar_value": 4000.0
    #}


