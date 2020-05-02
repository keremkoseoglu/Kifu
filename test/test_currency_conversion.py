from model.currency import CurrencyConverter

cc = CurrencyConverter()
x = cc.get_local_conversion_rate("USD")
print("1 USD = " + str(x))

x = cc.convert_to_local_currency(100, "USD")
print("100 USD = " + str(x))

x = cc.convert_to_foreign_currency(100, "USD")
print("100 TRY = " + str(x))
