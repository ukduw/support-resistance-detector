# input format:
    # a, b, c, d, e, f, g...

def symbol_cli():
    default = 4000
    print("Input watchlist")

    while True:
        user_entry = input(f"Paste symbol list (separate symbols by ','): ").upper()
        dollar_value = input(f"Position dollar value [{default}]: ")

        symbol_dict = {"tickers": user_entry.split(", ")}

        count = len(symbol_dict.tickers)

        symbol_dict["dollar_value"] = float(dollar_value or default)


        print(f"({count})")
        for key in symbol_dict:
            print(key, symbol_dict[key])

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
    
    return symbol_dict


# output format:
    # {
    # "tickers": ['A', 'B', 'C', 'D', ...],
    # "dollar_value": 4000.0
    # }


if __name__ == "__main__":
    symbol_cli()


