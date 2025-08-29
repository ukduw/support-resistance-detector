# alpaca api call for 5(?) days of historical data
    # high, low, open, close, indicators (rsi, ...)
# determine support/resistance levels - probably need to increase sensitivity for granular/weak levels

# need logic to determine:
    # levels closest to 5% of current price, within 10%
    # what is equidistant?
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