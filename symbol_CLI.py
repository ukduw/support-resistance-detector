
def symbol_cli():
    print("Input watchlist")

    while True:
        symbol_list = input(f"Enter symbol list, separated by commas: ").upper().split(", ")
        print(f"({len(symbol_list)}) {symbol_list}")

        while True:
            cont = input("Is this correct? (y/n): ").stip().lower()
            if cont == "n":
                break
            elif cont == "y":
                break
            else:
                print(f"'{cont}' is not a valid input. Re-enter (y/n)")
        
        if cont == "y":
            break
    
    return symbol_list


