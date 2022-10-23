import requests
import json


def currency_verification(currency: str) -> dict:
    """
    Checks the correctness of the entered currency
    :param currency: the currency that you have
    :return: a json dictionary that contains all information about currencies, in particular the exchange rate
    """
    response = requests.get(f"http://www.floatrates.com/daily/{currency}.json")

    if not response:
        print("incorrect currency entry")
        exit(1)

    return json.loads(response.text)


def caching_dollars_and_euros(json_currencies: dict, currency: str) -> dict:
    """
    Save the exchange rates for USD and EUR
    (these are the most popular ones, so it's good to have rates for them in advance)
    :param json_currencies: a json dictionary that contains all information about currencies
    :param currency: the currency that you have
    :return: currency cached dictionary
    """
    currency_dictionary = {}

    if currency != "usd":
        currency_dictionary["usd"] = float(json_currencies["usd"]["inverseRate"])
    if currency != "eur":
        currency_dictionary["eur"] = float(json_currencies["eur"]["inverseRate"])

    return currency_dictionary


def main():
    my_currency = input().lower()
    # A json dictionary that contains all information about currencies
    json_currencies = currency_verification(my_currency)
    # Dictionary of cached currencies
    currency_dictionary = caching_dollars_and_euros(json_currencies, my_currency)

    while True:
        exchange_currency = input().lower()

        if exchange_currency == "":
            exit(0)

        try:
            my_money = float(input())
        except ValueError:
            print("Incorrect entry of your amount of money")
            break

        print("Checking the cache...")

        if exchange_currency in currency_dictionary.keys():
            print("Oh! It is in the cache!")
            amount_of_money = my_money / currency_dictionary[exchange_currency]
        else:
            print("Sorry, but it is not in the cache!")
            inverse_rate = float(json_currencies[exchange_currency]["inverseRate"])
            amount_of_money = my_money / inverse_rate
            # Save the exchange rates
            currency_dictionary[exchange_currency] = float(json_currencies[exchange_currency]["inverseRate"])

        print(f"You received {round(amount_of_money, 2)} {exchange_currency.upper()}.")


if __name__ == "__main__":
    main()
