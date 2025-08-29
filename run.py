from symbol_CLI import symbol_cli

# wrapper

# run symbol-CLI
# call support-resistance-detector with inputted list as argument
# call parameter-writer with nearest appropriate levels dict as argument
    # outputs json, usable with hybrid-tradebot

if __name__ == "main":
    symbols = symbol_cli()
    levels_dict = support_resistance_detector(symbols)
    parameter_writer(levels_dict)