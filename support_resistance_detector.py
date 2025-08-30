# alpaca api call for 5(? less? 6?) days of historical data
    # high, low, open, close, indicators (rsi, ...)

# determine support/resistance levels - probably need to increase sensitivity for granular/weak levels
    #

# need logic to determine:
    # levels closest to 5% of current price, within 10%
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


