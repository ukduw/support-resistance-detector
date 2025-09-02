
def symbol_cli():
    default = 4000
    print("Input watchlist")

    while True:
        symbol_list = input(f"Enter symbol list, separated by commas: ").upper().split(", ")
        print(f"({len(symbol_list)}) {symbol_list}")
        dollar_value = input(f"Position dollar value [{default}]: ")

        while True:
            cont = input("Is this correct? (y/n): ").strip().lower()
            if cont == "n":
                break
            elif cont == "y":
                break
            else:
                print(f"'{cont}' is not a valid input. Re-enter (y/n)")
        
        if cont == "y":
            break
    
    return {"symbol_list": symbol_list, "dollar_value": float(dollar_value or default)}


# re-write to prompt user to input 6 different lists
    # fetch 5, 4, 3, 2, 1, and 0 days back
        # 0 days means intraday only
        # all other ones means intraday + x days
            # use this to calculate lookback minutes in support_resistance_detector
            # e.g. 2 days = 11:45 (intra) + 16hr (full day) * 2 (day count) = 43.75hrs
    
    # account for blank entry on certain day
        # e.g. if len(symbol_list) == 0...