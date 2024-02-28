from fastapi import FastAPI, HTTPException
import requests
from datetime import *
# comment 02
app = FastAPI()
 
API_BASE_URL = "https://api.exchangerate-api.com/v4/latest/"
COINBASE_API_URL = "https://api.coinbase.com/v2/currencies/crypto"
COINBASE_RATES = "https://api.coinbase.com/v2/exchange-rates/"
COINBASE_FIAT = "https://api.coinbase.com/v2/currencies"
FREECURRENCYAPI = "https://api.freecurrencyapi.com/v1/historical?apikey=fca_live_7dHeSfDiffz0YIQcp86XBN45JExNt6GHsDY9n5m0"
 

async def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    response = requests.get(f"{API_BASE_URL}{from_currency.upper()}") 
    if response.status_code == 200:
        data = response.json()
        if to_currency.upper() in data["rates"]:
            return data["rates"][to_currency.upper()]
        else:
            raise HTTPException(status_code=400, detail="To currency not supported")
    else:
        raise HTTPException(status_code=400, detail="From currency not supported")


@app.get("/exchange_rate")
async def exchange_rate(from_currency: str, to_currency: str) -> dict:
    rate = await get_exchange_rate(from_currency, to_currency)
    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "exchange_rate": rate,
    }

@app.get("/convert_amount")
async def convert_amount(from_currency: str, to_currency: str, amount: float) -> dict:
    rate = await get_exchange_rate(from_currency, to_currency)
    converted_amount = amount * rate
    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "converted_amount": converted_amount,
    }

@app.get("/check_password_strength")
async def check_password_strength(password: str) -> dict:
   
    #coded by: Philip Hushani
    specialc = '!@£$%^#&*()_-~?><'
    p_uppercase = any(char.isupper() for char in password)
    p_lowercase = any(char.islower() for char in password)
    p_digit = any(char.isdigit() for char in password)
    plength = len(password) >= 8
    special_c = any(char in specialc for char in password)
 
    return {
        "User_has_strong_password": p_uppercase and p_lowercase and p_digit and plength and special_c
    }


@app.get("/available_currencies")
async def available_currencies() -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}USD")
        if response.status_code == 200:
            data = response.json()
            base_currency = data["base"]
            available_currencies = list(data["rates"].keys())
            return {"base_currency": base_currency, "available_currencies": available_currencies}
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch available currencies")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

 
#Coded by: Alexander Naskinov

@app.get("/available_crypto")
async def available_crypto() -> dict:
   
    #Coded by: Bette Beament
    #This endpoint allows you to see what crypto-currencies are available
   
    try:
        response = requests.get(COINBASE_API_URL)
        if response.status_code == 200:
            data = response.json()
            crypto_currencies = [{"Crypto ID :": currency["code"], "Crypto name : ": currency["name"]} for currency in data["data"]]
            return {"Crypto curriences :": crypto_currencies}
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch crypto currencies")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
async def get_usd_rate() -> dict:
    # """
    # Coded by: Tomasz Wisniewski
    # This function downloads rates for USD currency.
    # """
    response = requests.get(f"{COINBASE_RATES}")
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch USD rates")
   
@app.get("/convert_crypto")
async def convert_crypto(from_crypto: str, to_currency: str, amount: float) -> dict:
    # """
    # Coded by: Tomasz Wisniewski & Bette Beament
    # This endpoint allows you to convert crypto into any currency.
    # This endpoint includes a function to display an error when an invalid crypto currency has been entered.
    # """
    try:
        check_result = await check_all_currencies(from_crypto)
        if "error_message" in check_result:
            raise HTTPException(status_code=400, detail=check_result["error_message"])
 
        crypto_rate = await get_usd_rate()
        ex_rate = await exchange_rate(to_currency, "USD")
        rate_to_USD = float(ex_rate["exchange_rate"])
        rate_from_USD = float(crypto_rate['rates'][from_crypto])
        rate_crypto = rate_to_USD * rate_from_USD
        converted_amount = (1 / rate_crypto) * amount
        return {
            "crypto_currency": from_crypto.upper(),
            "fiat_currency": to_currency.upper(),
            "crypto_rate": rate_crypto,
            "amount": amount,
            "converted_amount": converted_amount,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 
@app.get("/update_orderbookdb_asset_price")
async def update_orderbookdb_asset_price(symbol: str, new_price: float) -> dict:
    # """
    # Coded by: Tomasz Wisniewski
    # This endpoint allows you to update price of asset in orderbook database.
    # """
    from sqlalchemy import create_engine, Table, Column, String, DateTime, Numeric, update, MetaData
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('mysql+pymysql://wiley:wiley123@a11e83d0d11d64c75a070bf9a91b8c6c-1320554700.us-east-1.elb.amazonaws.com/orderbook')
    metadata = MetaData()
    product_table = Table('Product', metadata,
        Column('symbol', String(16), primary_key=True),
        Column('price', Numeric(precision=15, scale=2)),
        Column('productType', String(12)),
        Column('name', String(128)),
        Column('lastUpdate', DateTime)
    )
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    try:
        session = Session()
        stmt = update(product_table).where(product_table.c.symbol == symbol).values(price=new_price)
        session.execute(stmt)
        session.commit()
        session.flush()
        return {"update_report": "success", "symbol": symbol, "new_price": new_price}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="An error occurred, make sure symbol exists and price is numeric")
    finally:
        session.close()
 
 
async def get_crypto_name(crypto_n: str) -> str:
    # """
    # Coded by: Tomasz Wisniewski
    # This function downloads all crypto names and extract required name.
    # """
    get_crypto_names = await available_crypto()
    if get_crypto_names.status_code == 200:
        crypto_names = get_crypto_names["Crypto curriences :"]
        for crypto_name in crypto_names:
            if crypto_name["Crypto ID :"] == crypto_n:
                c_name = crypto_name["Crypto name : "]
                return c_name
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch crypto name")
       
# @CODE : ADD ENDPOINT FOR INSERTING A CRYPTO CURRENCY INTO THE ORDERBOOK APP
# HINT: Make use of the convert_crypto function from above!
#       You will need to use the await keyword to wait for the result (otherwise it will run async and not wait for the result)
@app.get("/add_crypto_to_orderbook")
    # """
    # Coded by: Tomasz Wisniewski
    # This endpoint will insert a crypto currency into the orderbook app.
    # """
async def add_crypto_to_orderbook(crypto: str) -> dict:
    from sqlalchemy import create_engine, Table, Column, String, DateTime, Numeric, insert, MetaData
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime
    from decimal import Decimal
    engine = create_engine('mysql+pymysql://wiley:wiley123@a11e83d0d11d64c75a070bf9a91b8c6c-1320554700.us-east-1.elb.amazonaws.com/orderbook')
    crypto_data = await convert_crypto(crypto, "USD", 1)
    c_name = await get_crypto_name(crypto)
    crypto_price = Decimal(1/crypto_data["crypto_rate"]).quantize (Decimal ('.01'))
    try:
        metadata = MetaData()
        orderbook_table = Table('Product', metadata,
            Column('symbol', String(16), primary_key=True),
            Column('price', Numeric(precision=15, scale=2)),
            Column('productType', String(12)),
            Column('name', String(128)),
            Column('lastUpdate', DateTime)
        )
        metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        stmt = insert(orderbook_table).values(symbol=crypto, price=crypto_price, productType=c_name, name=crypto, lastUpdate=datetime.now().replace(microsecond=0))
        session.execute(stmt)
        session.commit()
        session.flush()
        return {"insert_report": "success", "symbol": crypto}
    except Exception as e:
        raise HTTPException(status_code=400, detail="An error occurred while inserting into orderbook")
    finally:
        session.close()

@app.get("/check_all_currencies")
async def check_all_currencies(currency_symbol: str) -> dict:
    """
    Coded by: Alex Naskinov
    This endpoint checks if a given crypto or fiat currency is tradable using the symbol value. (Uses COINBASE_RATES API)
    """
    try:
        response = requests.get(COINBASE_RATES)
        if response.status_code == 200:
            data = response.json()
            rates = data["data"]["rates"]
            currency_symbol_upper = currency_symbol.upper()  # Convert input to uppercase
       
            if currency_symbol_upper in rates:
                return {"message": "This currency is tradable"}
            else:
                return {"error_message": "This currency is not tradable"}
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch currency rates")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/compare_currencies")
async def compare_currencies(currency_1: str, currency_2: str) -> dict:
    try:
        if currency_1.upper() == currency_2.upper():
            return {
                "currency_1": currency_1.upper(),
                "currency_2": currency_2.upper(),
                "exchange_rate": 1,
                "amount_in_currency_2_with_one_unit_of_currency_1": 1,
                "message": "Both input values are the same",
                "value_message": "No difference in value"
            }
       
        response = requests.get(API_BASE_URL + currency_1.upper())
       
        if response.status_code == 200:
            data = response.json()
            conversion_rates = data["rates"]
           
            if currency_2.upper() in conversion_rates:
                rate_currency_2 = conversion_rates[currency_2.upper()]
                amount_in_currency_2 = 1 / rate_currency_2
               
                # Determine which currency is more valuable
                if rate_currency_2 < 1:
                    more_valuable_currency = currency_2.upper()
                    less_valuable_currency = currency_1.upper()
                    value_multiple = 1 / rate_currency_2
                    value_message = f"{currency_1.upper()} is {value_multiple:.2f} x less valuable than {currency_2.upper()}"
                elif rate_currency_2 > 1:
                    more_valuable_currency = currency_1.upper()
                    less_valuable_currency = currency_2.upper()
                    value_multiple = rate_currency_2
                    value_message = f"{currency_1.upper()} is {value_multiple:.2f} x more valuable than {currency_2.upper()}"
                else:
                    return {
                        "currency_1": currency_1.upper(),
                        "currency_2": currency_2.upper(),
                        "exchange_rate": rate_currency_2,
                        "amount_in_currency_2_with_one_unit_of_currency_1": amount_in_currency_2,
                        "message": "These currencies have the same value",
                        "value_message": "No difference in value"
                    }
 
                return {
                    "currency_1": currency_1.upper(),
                    "currency_2": currency_2.upper(),
                    "exchange_rate": rate_currency_2,
                    "amount_in_currency_2_with_one_unit_of_currency_1": amount_in_currency_2,
                    "message": f"{more_valuable_currency} is more valuable than {less_valuable_currency}",
                    "value_message": value_message
                }
            else:
                raise HTTPException(status_code=400, detail="One of the currencies is not supported")
        else:
            raise HTTPException(status_code=400, detail="Failed to fetch exchange rates/ currency not supported")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_historical_data(from_currency: str, to_currency: str) -> dict:
    # """
    # Coded by: Tomasz Wisniewski
    # This function downloads historical rate against USD for required currency.
    # """
    response = requests.get(f"{FREECURRENCYAPI}&base_currency={from_currency}&currencies={to_currency}")
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        raise HTTPException(status_code=400, detail="Failed to fetch USD the historical data")

async def new_price_vs_old_price(new_price: float, old_price: float, from_currency: str, to_currency: str) -> dict:
    # """
    # Coded by: Tomasz Wisniewski
    # This function compares old_price vs new_price and returns the final result.
    # It was created as I need assign prices seperately for currency and crypto
    # """
    global percentage
    percentage = 0
    if old_price > new_price:
        percentage = round((old_price - new_price) / old_price, 3)
        return {"message": f"Today {from_currency.upper()} is worth {round(old_price-new_price,4)} more than yesterday against {to_currency.upper()}.",
                "price": f"Todaya's price for {from_currency.upper()} = {1*new_price} {to_currency.upper()}",
                "percentage": f"Percentage change = {percentage*100}%"}
    if old_price < new_price:
        percentage = round((new_price - old_price) / new_price, 3)
        return {"message": f"Today {from_currency.upper()} is worth {round(new_price-old_price,4)} less than yesterday against {to_currency.upper()}",
                "price": f"Todaya's price for {from_currency.upper()} = {1*new_price} {to_currency.upper()}",
                "percentage": f"Percentage change = -{percentage*100}%"}
    else:
        return {"message": f"{from_currency.upper()} price hasn't change since yesterday against {to_currency.upper()}.",
                "price": f"Todaya's price for {from_currency.upper()} = {1*new_price} {to_currency.upper()}",
                "percentage": f"Percentage change = {percentage*100}"}

@app.get("/check_yesterdays_price")
async def check_yesterdays_price(from_currency: str, to_currency: str) -> dict:
    # """
    # Coded by: Tomasz Wisniewski and Bette Beament
    # This endpoint will compare current price with the price from previous day against USD
    # """
    y_day = []
    today_d = date.today()
    y_day.append(today_d - timedelta(days = 1))
    yesterday = y_day[0]
    try:
        if len(from_currency) > 7 or len(to_currency) > 7:
            raise HTTPException(status_code=404, detail="This cannot be currency or crypto. Max 7 letters allowed! If you need to find out the ID use /'Check Crypto' or /'Available currencies' endpoint.")
        check_1st_currency = await available_currencies()
        if from_currency.upper() not in check_1st_currency['available_currencies']:
            raise HTTPException(status_code=404, detail=(f"The ID '{from_currency.upper()}' is NOT on the market."))
        else:
            check_2nd_currency = await available_currencies()
            if to_currency.upper() not in check_2nd_currency['available_currencies']:
                raise HTTPException(status_code=404, detail=(f"The ID '{to_currency.upper()}' is NOT on the market."))
        #check_crypto = await available_crypto(from_currency)
        check_result = await check_all_currencies(from_currency)
        print(len(from_currency))
        if "error_message" in check_result:
            raise HTTPException(status_code=404, detail=check_result["error_message"])
        old_data = await get_historical_data(from_currency.upper(), to_currency.upper())
        old_price = round(old_data[str(yesterday)][to_currency.upper()],3)
        new_data = await exchange_rate(from_currency, to_currency)
        new_price = round(new_data['exchange_rate'],3)
        #
        verification = await new_price_vs_old_price(new_price, old_price, from_currency, to_currency)
        return verification
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="An error occurred while receiving data")

@app.post("/calculate_portfolio_value")
async def calculate_portfolio_value(holdings: dict, base_currency: str = "USD"):
    total_value = 0.0
    for currency, amount in holdings["holdings"].items():
        try:
            exchange_rate = await get_exchange_rate(base_currency, currency)
            total_value += amount * exchange_rate
        except HTTPException as e:
 
            print(f"Error for currency {currency}: {str(e)}")
 
    result = {"total_portfolio_value": total_value}
 
    if total_value > 2000:
        result["suggestion"] = "Consider investing in a diversified portfolio. Think about individual stocks and Exchange Traded Funds."
 
    if total_value > 5000:
        result["suggestion"] = "Explore investment options with higher returns. Think about Crypto currency and Bonds"
 
    if total_value > 10000:
        result["suggestion"] = "Consult with a financial advisor for personalized investment advice."
 
    if total_value > 50000:
        result["suggestion"] = "Diversify across different asset classes for long-term growth. Look into Real Estate."
 
    return result
