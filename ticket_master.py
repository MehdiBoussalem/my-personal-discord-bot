import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

key = config['TICKETMASTER']['key']
secret_key = config['TICKETMASTER']['secret_key']
reqSession = requests.Session()


def getEventsID(artist):
    params = {'apikey': key, 'secret': secret_key, 'keyword': artist, "locale": "*"}
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    reponse = reqSession.get(url, params=params).json()
    return reponse['_embedded']['events'][0]["id"]


def getEventInfo(event_id):
    params = {'apikey': key, 'secret': secret_key}
    url = 'https://app.ticketmaster.com/discovery/v2/events/' + event_id + '.json'
    reponse = reqSession.get(url, params=params).json()
    return reponse




print(getEventInfo(getEventsID("against the current")))
