###############################################################################################################################################
##############
############## CURRENCY CONVERTER BOT FOR FACEBOOK MESSENGER - BOT
##############
############## Welcome!
##############
############## This is the bot file of our product.
##############
############## It is accessed each time the bot responds something to the user.
##############
##############

###############################################################################################################################################

# NECESSARY IMPORTS
import requests
import json
FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/v5.0/me/'

# CREATION OF BOT CLASS
class Bot(object):
    def __init__(self, access_token, api_url=FACEBOOK_GRAPH_URL):
        self.access_token = access_token
        self.api_url = api_url

    def send_text_message(self, psid, message, messaging_type="RESPONSE"):
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
          "messaging_type": messaging_type,
          "recipient": {'id': psid},
          "message": {"text": message}
        }

        params = {'access_token': self.access_token}
        self.api_url = self.api_url + 'messages'
        response = requests.post(self.api_url, headers=headers, params=params, data=json.dumps(data))
        print(response.content)


# TEST THE BOT (THIS IS NOT USED AND JUST KEPT HERE FOR DEBUGGING IN CASE A PROBLEM OCCURS)
#bot = Bot('EAAILCvOB3nsBAB0uDjD9xKF9pLGvDPwz1SJX2XDp38ZCMGuE2DdCmu3RBRL2ZAdCZCwiAxbc9OmS3lsaZCJlBqc9zOahvsZAT67GiXlHtgt5bOoaNwWZApxLbzgdZACJknPE5ZC7bvddP9YV08SjoRZABWeiWfpneIGO3lF64l9na2xgq24ZBkIGoI')
#bot.send_text_message(2952943251392301, 'Testing..')
