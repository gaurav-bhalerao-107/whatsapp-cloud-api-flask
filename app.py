from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import json
from bson.objectid import ObjectId
from datetime import datetime

# 
class JSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, ObjectId):
      return str(o)
    if isinstance(o, datetime):
      return o.strftime('%Y-%m-%dT%H:%M:%SZ')
    return json.JSONEncoder.default(self, o)


# 
app = Flask(__name__)
app.json_encoder = JSONEncoder
cors = CORS(app)


# 
load_dotenv()
env = os.environ.get


# 
class Config(object):
  SECRET_KEY = env("SECRET_KEY")
  PHONE_NUMBER_ID = env("PHONE_NUMBER_ID")
  RECIPIENT_PHONE_NUMBER = env("RECIPIENT_PHONE_NUMBER")
  BEARER_TOKEN = env("BEARER_TOKEN")

app.config.from_object(Config())


# 
def send_whatsapp_message():
  version = 'v14.0'
  phone_number_id = app.config['PHONE_NUMBER_ID']
  url = "https://graph.facebook.com/{}/{}/messages".format(version, phone_number_id)
  
  recipient_phone_number = '91{}'.format(app.config['RECIPIENT_PHONE_NUMBER'])
  payload = json.dumps({
    "messaging_product": "whatsapp",
    "to": recipient_phone_number,
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": {
        "code": "en_US"
      }
    }
  })

  bearer_token = app.config['BEARER_TOKEN']
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {}'.format(bearer_token)
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)

send_whatsapp_message()

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)