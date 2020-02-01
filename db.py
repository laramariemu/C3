###############################################################################################################################################
##############
############## CURRENCY CONVERTER BOT FOR FACEBOOK MESSENGER - DATABASE FUNCTIONS
##############
############## Welcome!
##############
############## This is the database functions file of our product.
##############
############## Here, the database is created. Users information that is saved here: User-ID, desired currency, desired converted amount,
############## real-time exchange rate for currency, the requested product and its current average price.
##############
############## It is accessed each time a function is called that puts something in the database or gets a certain value out of it.
############## It is updated each time the user makes a new request.
############## Also, all computations for the currency conversion are done here in the created table.
############## Furthermore, everytime we download current exchange rates and the statistical data this happens here.
##############

###############################################################################################################################################

# NECESSARY IMPORTS
import requests
import re
import sqlite3

# NAME OF DATABASE THAT IS TO BE CREATED
DB_NAME = 'users.db'

#CREATING CONNECTION TO DB AND A TABLE IN IT
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def main():
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                        ID integer PRIMARY KEY,
                                        currency text,
                                        yen_amount real,
                                        conversion_rate real,
                                        converted_amount real,
                                        requested_product text,
                                        requested_product_price real
                                    );"""
    conn = create_connection(DB_NAME)
    if conn is not None:
        create_table(conn, sql_create_users_table)
    else:
        print("Error! cannot create the database connection.")


# FUNCTION TO ADD NEW USER IN TABLE
def insert_user(ID):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO users VALUES (:ID, :currency, :yen_amount, :conversion_rate, :converted_amount, :requested_product, :requested_product_price)""",
              {'ID': ID, 'currency': 'JPY', 'yen_amount': -99, 'conversion_rate': -99, 'converted_amount': -99, 'requested_product':'default', 'requested_product_price': -99})
    except sqlite3.Error as e:
        print ('e')


# FUNTION TO CHECK WHETHER A CERTAIN USER IS ALREADY IN THE TABLE
def check_if_user_exists(ID):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT ID FROM users WHERE ID=:ID", {'ID': ID})
            return cur.fetchall()
    except sqlite3.Error as e:
        print ('e')


# FUNCTION TO UPDATE THE AMOUNT THAT IS SUPPOSED TO BE CONVERTED
def update_yen_amount(ID,yen_amount):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("""UPDATE users SET yen_amount = :yen_amount
            WHERE ID=:ID""", {'ID':ID, 'yen_amount': yen_amount})
    except sqlite3.Error as e:
        print ('e')


# FUNCTION TO UPDATE THE CURRENCY THAT THE REQUESTED AMOUNT SHOULD BE CONVERTED INTO
def update_currency(ID,currency):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("""UPDATE users SET currency = :currency
            WHERE ID=:ID""", {'ID':ID, 'currency': currency})
    except sqlite3.Error as e:
        print ('e')


# FUNCTION TO GET THE CURRENT EXCHANGE RATES OUT OF THE INTERNET (CURRENTLY UPDATED EVERY 60MIN)
def ExRate(to_currency):
    url = 'https://api.exchangerate-api.com/v4/latest/JPY'
    response = requests.get(url)
    data = response.json()
    all_rates = data.get('rates')
    #print(all_rates)
    req_rate = all_rates.get(to_currency)
    return req_rate


# FUNCTION TO UPDATE THE APPLICABLE CONVERSION RATE IN THE TABLE
def update_conversion_rate(ID):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT conversion_rate FROM users WHERE ID=:ID", {'ID': ID})
            conversion_rate = cur.fetchone()
            conversion_rate = conversion_rate[0]
            cur.execute("SELECT currency FROM users WHERE ID=:ID", {'ID': ID})
            currency = cur.fetchone()
            currency = currency[0]
            update = ExRate(currency)
            if update is not conversion_rate:
                cur.execute("""UPDATE users SET conversion_rate = :update
                WHERE ID=:ID""", {'ID':ID, 'update': update})
    except sqlite3.Error as e:
        print ('e')


# FUNCTION TO CALCULATE WHAT THE CONVERTED AMOUNT IS
def calculate_converted_amount(ID):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT yen_amount FROM users WHERE ID=:ID", {'ID': ID})
            yen_amount = cur.fetchone()
            yen_amount = yen_amount[0]
            cur.execute("SELECT conversion_rate FROM users WHERE ID=:ID", {'ID': ID})
            conversion_rate = cur.fetchone()
            conversion_rate = conversion_rate[0]
            con = yen_amount*conversion_rate
            conv = round(con, 2)
            cur.execute("UPDATE users SET converted_amount=:conv WHERE ID=:ID", {'conv':conv, 'ID':ID})
    except sqlite3.Error as e:
        print ('e')


# FUNCTION THAT RETURNS THE CONVERTED AMOUNT BACK TO THE BOT
def return_converted_amount(ID):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT converted_amount FROM users WHERE ID=:ID", {'ID': ID})
            converted_amount = cur.fetchone()
            converted_amount = converted_amount[0]
            return converted_amount
    except sqlite3.Error as e:
        print ('e')


# FUNCTION TO DETERMINE WHAT CURRENCY A CERTAIN USER CURRENTLY WANTS HIS/HER AMOUNT TO BE CONVERTED INTO
def get_users_currency(ID):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT currency FROM users WHERE ID=:ID", {'ID': ID})
            users_currency = cur.fetchone()
            users_currency = users_currency[0]
            if 'EUR' in users_currency:
                return re.sub('EUR','Euro', users_currency)
            if 'USD' in users_currency:
                return re.sub('USD','US-Dollar', users_currency)
            if 'CNY' in users_currency:
                return re.sub('CNY','Chinese Yuan', users_currency)
            if 'JPY' in users_currency:
                return re.sub('JPY','Japanese Yen', users_currency)
            return users_currency
    except sqlite3.Error as e:
        print ('e')


# FUNCTION TO INSERT A PRODUCT REQUEST BY A USER
def update_requested_product(ID,product):
    try:
        conn = create_connection(DB_NAME)
        with conn:
            cur = conn.cursor()
            request = product
            cur.execute("""UPDATE users SET requested_product=:request
            WHERE ID=:ID""", {'ID':ID, 'request':request})
    except sqlite3.Error as e:
        print ('e')


# THIS JUST HAS TO BE RUN THE FIRST TIME BEFORE STARTING THE CHATBOT (IN ORDER TO CREATE DATABASE)
if __name__ == '__main__':
    main()
