import meteofrance_api
import requests
import configparser
from meteofrance_api import *

config = configparser.ConfigParser()
config.read('config.ini')

client = meteofrance_api.MeteoFranceClient()
argenteuil = client.get_forecast_for_place(place="95100",language="fr")
print(argenteuil)
