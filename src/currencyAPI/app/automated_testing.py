# # Testing c374team23 endpoints

import requests
import tracemalloc
import asyncio

test_successful = 0
test_failed = 0

# Testing /check_password_strength endpoint
async def run_test_check_password(url: str, password: str) -> dict:
    global test_successful
    global test_failed
    params = {"password": password}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/check_password_strength"
# TEST 01
x = run_test_check_password(url, "password")
asyncio.run(x)
# TEST 02
x = run_test_check_password(url, "Password")
asyncio.run(x)
# TEST 03
x = run_test_check_password(url, "Password123")
asyncio.run(x)
# TEST 04
x = run_test_check_password(url, "Password123%")
asyncio.run(x)
# TEST 05
x = run_test_check_password(url, "password123")
asyncio.run(x)
# TEST 06
x = run_test_check_password(url, "pass")
asyncio.run(x)
# TEST 07
x = run_test_check_password(url, "123456789")
asyncio.run(x)

# Testing /available_currencies endpoint
async def run_test_available_currencies(url: str,) -> dict:
    global test_successful
    global test_failed
    #params = {"crypto_param": password}
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/available_currencies"
# TEST 01
x = run_test_available_currencies(url)
asyncio.run(x)

# Testing /available_crypto endpoint
async def run_test_available_crypto(url: str,) -> dict:
    global test_successful
    global test_failed
    #params = {"crypto_param": password}
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/available_crypto"
# TEST 01
x = run_test_available_crypto(url)
asyncio.run(x)

# Testing /convert_crypto endpoint
async def run_test_convert_crypto(url: str, from_currency: str, to_currency: str, amount: int) -> dict:
    global test_successful
    global test_failed
    params = {"from_crypto": from_currency, "to_currency": to_currency, "amount": amount}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/convert_crypto"
# TEST 01
x = run_test_convert_crypto(url, "BTC", "GBP", 100)
asyncio.run(x)
# TEST 02
x = run_test_convert_crypto(url, "btc", "GBP", 100)
asyncio.run(x)
# TEST 03
x = run_test_convert_crypto(url, "BTC", "gbp", 100)
asyncio.run(x)
# TEST 04
x = run_test_convert_crypto(url, "BTC", "GBP", 3)
asyncio.run(x)
# TEST 05
x = run_test_convert_crypto(url, "BTCC", "GBP", 3)
asyncio.run(x)
# TEST 06
x = run_test_convert_crypto(url, "BTC", "GBPK", 3)
asyncio.run(x)

# Testing /update_orderbookdb_asset endpoint
async def run_test_update_orderbookdb_asset(url: str, symbol: str, new_price: float) -> dict:
    global test_successful
    global test_failed
    params = {"symbol": symbol, "new_price": new_price}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/update_orderbookdb_asset_price"
# TEST 01
x = run_test_update_orderbookdb_asset(url, "BTC", 101)
asyncio.run(x)
# TEST 02
x = run_test_update_orderbookdb_asset(url, "APL", 102)
asyncio.run(x)
# TEST 03
x = run_test_update_orderbookdb_asset(url, "apl", 103)
asyncio.run(x)
# TEST 04
x = run_test_update_orderbookdb_asset(url, "APL", 103.4)
asyncio.run(x)
# TEST 05
x = run_test_update_orderbookdb_asset(url, "APL", -105)
asyncio.run(x)
# TEST 06
x = run_test_update_orderbookdb_asset(url, "APL", 999999999999999999996)
asyncio.run(x)
# TEST 07
x = run_test_update_orderbookdb_asset(url, "APL", -999999999999999999997)
asyncio.run(x)
#print(test_failed)
#print(test_successful)

# Testing /add_crypto_to_orderbook endpoint
async def run_test_add_cryptro_to_orderbook(url: str, crypto: str) -> dict:
    global test_successful
    global test_failed
    params = {"crypto": crypto}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/add_crypto_to_orderbook"
# TEST 01
x = run_test_add_cryptro_to_orderbook(url, "BTC")
asyncio.run(x)
# TEST 02
x = run_test_add_cryptro_to_orderbook(url, "APL")
asyncio.run(x)
# TEST 03
x = run_test_add_cryptro_to_orderbook(url, "rpl")
asyncio.run(x)
# TEST 04
x = run_test_add_cryptro_to_orderbook(url, "RPL")
asyncio.run(x)
# TEST 05
x = run_test_add_cryptro_to_orderbook(url, "RPLRPLRPLRPLRPLRPLRPLRPLRPLRPL")
asyncio.run(x)
# TEST 06
x = run_test_add_cryptro_to_orderbook(url, 999)
asyncio.run(x)
# TEST 07
x = run_test_add_cryptro_to_orderbook(url, "Litecoin")
asyncio.run(x)
#print(test_failed)
#print(test_successful)

# Testing /check_all_currencies endpoint
async def run_test_check_all_currencies(url: str, crypto_symbol: str) -> dict:
    global test_successful
    global test_failed
    params = {"crypto_symbol": crypto_symbol}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/check_all_currencies"
# TEST 01
x = run_test_check_all_currencies(url, "BTC")
asyncio.run(x)
# TEST 02
x = run_test_check_all_currencies(url, "USD")
asyncio.run(x)
# TEST 03
x = run_test_check_all_currencies(url, "btc")
asyncio.run(x)
# TEST 04
x = run_test_check_all_currencies(url, "usd")
asyncio.run(x)
# TEST 05
x = run_test_check_all_currencies(url, "bttc")
asyncio.run(x)

# Testing /compare_currencies endpoint
async def run_test_compare_currencies(url: str, currency_1: str, currency_2: str) -> dict:
    global test_successful
    global test_failed
    params = {"currency_1": currency_1, "currency_2": currency_2}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/compare_currencies"
# TEST 01
x = run_test_compare_currencies(url, "BTC", "GBP")
asyncio.run(x)
# TEST 02
x = run_test_compare_currencies(url, "btc", "GBP")
asyncio.run(x)
# TEST 03
x = run_test_compare_currencies(url, "BTC", "gbp")
asyncio.run(x)
# TEST 04
x = run_test_compare_currencies(url, "bitcoin", "GBP")
asyncio.run(x)
# TEST 05
x = run_test_compare_currencies(url, "BTCK", "GBP")
asyncio.run(x)

# Testing /check_yesterdays_price endpoint
async def run_test_check_yesterdays_price(url: str, from_currency: str, to_currency: str) -> dict:
    global test_successful
    global test_failed
    params = {"from_currency": from_currency, "to_currency": to_currency}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)    
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/check_yesterdays_price"
# TEST 01
x = run_test_check_yesterdays_price(url, "BTC", "GBP")
asyncio.run(x)
# TEST 02
x = run_test_check_yesterdays_price(url, "btc", "GBP")
asyncio.run(x)
# TEST 03
x = run_test_check_yesterdays_price(url, "BTC", "gbp")
asyncio.run(x)
# TEST 04
x = run_test_check_yesterdays_price(url, "bitcoin", "GBP")
asyncio.run(x)
# TEST 05
x = run_test_check_yesterdays_price(url, "bitcoinbitcoin", "GBP")
asyncio.run(x)
# TEST 06
x = run_test_check_yesterdays_price(url, "btc", "poundpoundpound")
asyncio.run(x)
# TEST 07
x = run_test_check_yesterdays_price(url, "btc", "pound")
asyncio.run(x)

# Testing /calculate_portfolio_value endpoint
async def run_test_calculate_portfolio_value(url: str, base_currency: str , data_01: dict) -> dict:
    global test_successful
    global test_failed
    params = {"base_currency": base_currency, "holdings": data_01}
    response = requests.post(url, json=params)
    if response.status_code == 200:
        print(response)
        print(response.json())
        test_successful +=1
    else:
        print("Request failed with status code:", response.status_code)
        
        print(response.json())   
        test_failed +=1

url = "https://c374team23dev-currencyapi.computerlab.online/calculate_portfolio_value"
# TEST 01
data_01 = {
"cad": 3300.0,
"EUR": 500.0,
"GBP": 300.0
}
# TEST 02
data_02 = {
"CDA": 3300.0,
"ERU": 500.0,
"PGB": 300.0
}
# TEST 03
data_03 = {
"CADA": 3300.0,
"EUR": 500.0,
"GBP": 300.0
}
# TEST 04
data_04 = {
"": 3300.0,
"EUR": 500.0,
"GBP": 300.0
}
# TEST 05
data_05 = {
"CAD": 3300.0,
"EUR": 500.0,
"GBP": 300.0
}
# TEST 06
data_06 = {
"CAD": 3300.0,
"EUR": 500.0,
"GBP": 300.0
}
# TEST 01
x = run_test_calculate_portfolio_value(url, "GBP", data_01)
asyncio.run(x)
# TEST 02
x = run_test_calculate_portfolio_value(url, "EUR", data_02)
asyncio.run(x)
# TEST 03
x = run_test_calculate_portfolio_value(url, "gbp", data_03)
asyncio.run(x)
# TEST 04
x = run_test_calculate_portfolio_value(url, "GBPa", data_04)
asyncio.run(x)
# TEST 05
x = run_test_calculate_portfolio_value(url, "GBP", data_05)
asyncio.run(x)
# TEST 06
x = run_test_calculate_portfolio_value(url, "USD", data_06)
asyncio.run(x)

# Printing numbers of succesful and failed tests
print(f"Unsuccessful tests: {test_failed}")
print(f"Successful tests: {test_successful}")

# Saving tests results to the file 'tests_results.csv'
ct = datetime.datetime.now()
dd_month = str(ct.month)
curr_time = time.strftime("%H:%M:%S", time.localtime())
if len(dd_month) < 2:
    dd_month="0"+str(ct.month)
with open("tests_report.csv", "a") as tests_report:
    tests_report_str =f"\n| {ct.year}-{dd_month}-{ct.day} "    
    tests_report_str +=f"| {curr_time} |"
    tests_report_str +=f" " * (16-len(str(test_successful)))
    tests_report_str +=f" {test_successful} |"
    tests_report_str +=f" " * (12-len(str(test_failed)))
    tests_report_str +=f" {test_failed} |\n"
    tests_report_str +=f"-" * 59
    tests_report.write(tests_report_str)
    print("Testing report saved to file 'tests_report.csv'.")
