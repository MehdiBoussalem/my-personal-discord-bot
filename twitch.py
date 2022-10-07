import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"


reqSession = requests.Session()
url='https://id.twitch.tv/oauth2/token?client_id=' + config['TWITCH']['twitch_client_id'] + '&client_secret=' + config['TWITCH']['twitch_client_secret'] +  '&grant_type=client_credentials'

token = reqSession.post(url).json()['access_token']
API_HEADERS = {
    'Client-Id': config['TWITCH']['twitch_client_id'],
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Authorization': 'Bearer ' + token
}



def checkUser(userID):  # returns true if online, false if not
    url = TWITCH_STREAM_API_ENDPOINT_V5.format(userID)

    try:
        req = reqSession.get(url, headers=API_HEADERS)
        jsondata = req.json()
        if 'stream' in jsondata:
            if jsondata['stream'] is not None:  # stream is online
                return True
            else:
                return False
    except Exception as e:
        print("Error checking user: ", e)
        return False

def getUserId(user):
    url = 'https://api.twitch.tv/helix/users?login=' + user
    req = reqSession.get(url, headers=API_HEADERS)
    jsondata = req.json()
    return jsondata['data'][0]['id']
def getUserInformation(user):
    url = 'https://api.twitch.tv/helix/users?login=' + user
    req = reqSession.get(url, headers=API_HEADERS)
    jsondata = req.json()
    return jsondata['data'][0]

def getChannelInformation(user):
    url = 'https://api.twitch.tv/helix/channels?broadcaster_id=' + getUserId(user)
    req = reqSession.get(url, headers=API_HEADERS)
    jsondata = req.json()
    return jsondata
def getStreamInformation(user):
    url = 'https://api.twitch.tv/helix/streams?user_id=' + getUserId(user)
    req = reqSession.get(url, headers=API_HEADERS)
    jsondata = req.json()
    return jsondata

def isStreaming(user):
    return getStreamInformation(user)['data'] != []

