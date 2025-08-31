# alpaca api call for 5(? less? 6?) days of historical data
    # high, low, open, close, indicators (rsi, ...)
    # decide between 5min and 15min data

# determine support/resistance levels - probably need to increase sensitivity for granular/weak levels
# levels should have x% bounds - i.e. candles shouldn't have to bounce off a price perfectly to contribute to a level's count
    # if so, using the upper and lower bound of 2 levels for entry/exit will increase risk %
    # level * bound% is the variable that needs to be evaluated with the below logic

# gist:
    # pivot points (most common method):
        # based on previous levels (prev day high, low, close)
        # pivot = (high + low + close) / 3
            # R1 = 2 * pivot - low
            # S1 = 2 * pivote - high
            # R2 = pivot + (high - low)
            # S2 = pivot - (high - low)
            # ...
    # local maxima/minima:
        # local extrema over a sliding window of candlesticks
        # in other words, price points where price previously reversed


# need logic to determine:
    # levels closest to 5% of current price, within 10%
        # what if equidistant to 5%? e.g. 3 vs 7, 1 vs 9
    # just realized lower level should be 5-10% lower than the upper level used, not the intraday
    # if excessively close to current price, default to next closest level
    # if no upper in 5-10% range, default to <5 or >10?
    # if no lower in 5-10% range, just default to intraday??
# round to 4 significant figures

# build dict of entry/exit parameters per symbol
# return dict (to use in parameter-writer)


# symbols:
    #{"symbol_list": ["AAPL", "TSLA", ...], "dollar_value": 4000.0}

def support_resistance_detector(symbols):
    return


# desired output:
    #{
        #{"AAPL": [100.0, 95.0], "TSLA": [234.0, 223.0], ...},
        #"dollar_value": 4000.0
    #}


