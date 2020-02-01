###############################################################################################################################################
##############
############## CURRENCY CONVERTER BOT FOR FACEBOOK MESSENGER
##############
############## Welcome!
##############
############## This is the main file of our product.
############## It is running permanently (we are using pythonanywhere.com for that) and that accesses all other
############## documents (bot.py,utils.py,db.py and the database users.db).
############## Theoretically, a slgihtly modified version of this could also be used to built a chatbot for other applications
############## such as Line or WeChat.
##############
##############

###############################################################################################################################################

# NESESSARY IMPORTS
import json
from flask import Flask, request
from bot import Bot
import random
import re
import requests
from utils import analyze_input_amount, analyze_input_currency, analyze_input_product, inform_average_price, inform_quantity, inform_unit
from db import get_users_currency


# SECURITY RELEVANT TOKENS (if you run this, the security token has to be added to make it function)
PAGE_ACCESS_TOKEN = 'EAAILCvOB3nsBAB0uDjD9xKF9pLGvDPwz1SJX2XDp38ZCMGuE2DdCmu3RBRL2ZAdCZCwiAxbc9OmS3lsaZCJlBqc9zOahvsZAT67GiXlHtgt5bOoaNwWZApxLbzgdZACJknPE5ZC7bvddP9YV08SjoRZABWeiWfpneIGO3lF64l9na2xgq24ZBkIGoI'
SECURITY_TOKEN = 'XXX' # enter security token here

# LISTS AND DICTONARIES FOR SIMPLE CONVERSATIONS
GREETINGS = ['hi', 'hello', 'how are you', 'howdy', 'HI', 'Hi', 'Hello']
THX = ['thx', 'thank you', 'THX', 'thanks', 'Thank You', 'Thx', 'thanks a lot', 'thx!!', 'Thx!', 'thx!']
HOWDY = ['how are you', 'how are you?', 'How are you?', "how do you do?", 'how do you do?', 'howdy']
DEFAULTS = ['Right now, I am able to convert Japanese Yen into other currencies. Furthermore, I can provide you with average prices of typical purchases.', 'If you want me to convert a price, please state the price in Yen and the currency to convert it into. If you want to learn about average prices, state the name of the good your want to be informed about.', "I am still learning. I hope I will be able to reply to this request in the future.", "I am still learning. I hope I will be able to reply to this request in the future.", "I am still learning. I hope I will be able to reply to this request in the future.", "I am still learning. I hope I will be able to reply to this request in the future.", "I am still learning. I hope I will be able to reply to this request in the future."]
FUNCTIONALITY_REQUESTS = ['what can you do?', 'what are your skills?', 'how can you help me?', 'why do you exist?', 'what can you do']
FUNCTIONALITY_RESPONSES = ['Right now, I am able to convert Japanese Yen into other currencies. Furthermore, I can provide you with average prices of typical purchases.', 'If you want me to convert a price, please state the price in Yen and the currency to convert it into. If you want to learn about average prices, state the name of the good your want to be informed about.']
FAREWELL = ['bye', 'Goodbye', 'farewell', 'See you.', 'goodbye', 'bye bye', 'ciao']


#CREATION OF THE APPLICATION THAT CONNECTS THIS CODE WITH FACEBOOK MESSENGER
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == SECURITY_TOKEN:
            return str(challenge)
        return '400'

    else:
        data = request.data
        dati = json.loads(data)
        data = dati
        messaging_events = data['entry'][0]['messaging']
        bot = Bot(PAGE_ACCESS_TOKEN)
        for message in messaging_events:
            # these are the functions that analyze what users write and returns applicable info. refer to utils.py to see how they work in detail
            user_id = message['sender']['id']
            text_input = message['message'].get('text')
            response_text = random.choice(DEFAULTS)
            take_in = analyze_input_amount(user_id,text_input)
            conv_answer = analyze_input_currency(user_id,text_input)
            currency = get_users_currency(user_id)
            product = analyze_input_product(user_id,text_input)
            if product is not None:
                av_price = inform_average_price(user_id,product)
                quantity = inform_quantity(user_id,product)
                unit = inform_unit(user_id,product)

            if take_in is not None:
                response_text = 'The price you stated in Yen equals {} {}.'.format(conv_answer, currency)

            if product is not None and av_price is not None:
                response_text = 'Currently, the average price of {} {} of {} in Tokyo is {} Yen.'.format(quantity, unit, product, av_price)

            # these are a few --if --then statements for simple conversation. this could be improved with NLP to make the conversation more natural
            if text_input in GREETINGS:
                response_text = "Hello. Welcome to the Currency Converter Bot!"

            if text_input in HOWDY:
                response_text = "I'm great. Thanks! If you want me to convert a price, state the currency and the amount."

            if text_input in THX:
                response_text = "You're welcome!"

            if text_input in FAREWELL:
                response_text = "Have a good one!"

            elif text_input in FUNCTIONALITY_REQUESTS:
                response_text = random.choice(FUNCTIONALITY_RESPONSES)


        print('Message from user ID {} - {}'.format(user_id, text_input))
        bot.send_text_message(user_id, response_text)

        return '200'
