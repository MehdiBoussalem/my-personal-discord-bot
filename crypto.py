crypto_api_key="0941c8c6-52ed-4fa1-970f-f8e02ba0cda6"
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import csv


def get_btc_price():
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'start':'1',
    'limit':'2',
    'convert':'EUR'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': crypto_api_key,
  }

  session = Session()
  session.headers.update(headers)

  response = session.get(url, params=parameters)
  data = json.loads(response.text)




  btc_name = data['data'][0]['name']
  eth_name = data['data'][1]['name']

  btc_price = data['data'][0]['quote']['EUR']['price']
  btc_price = float(btc_price)
  btc_price = round(btc_price, 2)
  evolution= data['data'][0]['quote']['EUR']['percent_change_7d']
  evolution = float(evolution)
  evolution = round(evolution, 2)
  eth_price = data['data'][1]['quote']['EUR']['price']
  eth_price = float(eth_price)
  eth_price = round(eth_price, 2)
  eth_evolution= data['data'][1]['quote']['EUR']['percent_change_7d']
  eth_evolution = float(eth_evolution)
  eth_evolution = round(eth_evolution, 2)



  return btc_price, evolution, btc_name, eth_price, eth_evolution, eth_name

