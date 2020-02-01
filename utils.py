###############################################################################################################################################
##############
############## CURRENCY CONVERTER BOT FOR FACEBOOK MESSENGER - UTILS
##############
############## Welcome!
##############
############## This is the utils file of our product.
##############
############## It is accessed each time a function is called that analyzes the text input of the user.
############## Also, the data-preprocessing of the statistical data (average price) is done here.
##############
##############

###############################################################################################################################################


#NECESSARY IMPORTS
import re
import requests
import json
from db import check_if_user_exists, insert_user, update_yen_amount, update_currency, update_conversion_rate, calculate_converted_amount, return_converted_amount, ExRate, update_requested_product
import numpy as np
import pandas as pd

# SOME DICTIONARIES AND REFERENCE CASES
CURRENCIES = {'EUR': ['€', 'Euro', 'euro','EURO', 'Euros', 'euros', 'EUROS', 'EUR','euronen','europa','eoru'], 'USD':['US$','$','Dollar','US-Dollar','US-DOLLAR','dollar','us-dollar','usdollar','UsDollar','USD','dolla'], 'CNY': ['yuan', 'Chinese yuan', 'Yuan', 'renminbi','CNY','‎元','Chinese Yuan', 'Renminbi']}
EUR = CURRENCIES.get('EUR')
USD = CURRENCIES.get('USD')
CNY = CURRENCIES.get('CNY')
eur = re.compile('|'.join(EUR))
usd = re.compile('|'.join(USD))
cny = re.compile('|'.join(CNY))

# READ IN PRICE DATA FROM JAPANESE GOVERNMENTS WEBSITE
col_list=range(9,147)
data_prices = pd.read_excel("https://www.e-stat.go.jp/en/stat-search/file-download?statInfId=000031896568&fileKind=0", header=None, skiprows=33, nrows=1, usecols=col_list)
data_number_names = pd.read_excel("https://www.e-stat.go.jp/en/stat-search/file-download?statInfId=000031896568&fileKind=0", header=None, skiprows=10, nrows=1, usecols=col_list)
data_names = pd.read_excel("productnames.xlsx", header=0, nrows=138, usecols=[0,1,2,3,4])

# PREPROCESS STATISTICAL PRODUCT DATA (AVERAGE PRICES)
arr_prices = data_prices.values
prices=arr_prices.tolist()
lst_prices = prices[0]
data_names['price'] = lst_prices

arr_number_names = data_number_names.values
number_names = arr_number_names.tolist()
lst_number_names = number_names[0]

names = []
for row in data_names.name:
    names.append(row.lower())
good_names = re.compile('|'.join(names))

# DEFINITION OF IMPORTANT FUNCTIONS
# function that derives what amount the user wants to have converted
def analyze_input_amount(ID,text_input):
    amount=None
    ID = ID
    text_input = str(text_input)
    amount_match = [float(s) for s in text_input.split() if s.isdigit()]
    try:
        amount  = amount_match[0]
        amount = float(amount)
    except: amount = None

    if amount is not None:
        if not check_if_user_exists(ID):
            insert_user(ID)
        update_yen_amount(ID,amount)
        print('amount updated')
        return 'amount updated'

    else:
        print('no amount')
        return None

# function that checks to what currency the user wants his amount converted
def analyze_input_currency(ID,text_input):
    to_currency=None
    eur_currency_match = re.search(eur,text_input)
    usd_currency_match = re.search(usd,text_input)
    cny_currency_match = re.search(cny,text_input)
    conv_answer = None
    if eur_currency_match:
        to_currency = 'EUR'
    elif cny_currency_match:
        to_currency = 'CNY'
    elif usd_currency_match:
        to_currency = 'USD'
    else:
        to_currency = None
        conv_answer = None

    if to_currency is not None:
        if not check_if_user_exists(ID):
            insert_user(ID)
        update_currency(ID,to_currency)
        update_conversion_rate(ID)
        calculate_converted_amount(ID)
        conv_answer = return_converted_amount(ID)
        return conv_answer
    else:
        return None

# function that checks which product the user want the average price of
def analyze_input_product(ID,text_input):
    product=None
    ID = ID
    text_input = str(text_input)
    product_match = re.findall(good_names,text_input)
    if product_match:
        product_match_content = product_match[0]
        product = product_match_content
        update_requested_product(ID,product)
        return product
    else:
        return None

# function that matches the product with its average price
def inform_average_price(ID,product):
    ID = ID
    product = product
    av_price = None
    try:
        data = data_names[data_names['name'].isin([product])]
        dataa = data.values[0]
        av_price = dataa[5]
        return av_price
    except:
        return None

# function that determines the applicable quantitiy of the average price for the good
def inform_quantity(ID,product):
    ID = ID
    product = product
    quant = None
    try:
        data = data_names[data_names['name'].isin([product])]
        dataa = data.values[0]
        quant = dataa[1]
        try:
            quant = int(quant)
            return quant
        except:
            return quant
    except:
        return None

# function that determines the applicable unit of the average price for the good
def inform_unit(ID,product):
    ID = ID
    product = product
    unit = None
    try:
        data = data_names[data_names['name'].isin([product])]
        dataa = data.values[0]
        unit = dataa[2]
        return unit
    except:
        return None
