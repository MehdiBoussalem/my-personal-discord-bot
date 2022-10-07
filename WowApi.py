import requests
#CLIENT ID = 963ddc4e-34d1-43b9-b4d9-2892b6739599

#SECRET CLIENT ID = uTgaoTjJ2sWwbDZDC6cvGA8IH0smMYxbu6f6fzhP

client_id = '963ddc4e-34d1-43b9-b4d9-2892b6739599'
client_secret = 'uTgaoTjJ2sWwbDZDC6cvGA8IH0smMYxbu6f6fzhP'

#get token with cUrl command curl -u {client_id}:{client_secret} -d grant_type=client_credentials https://fr.warcraftlogs.com/oauth/token
#get token with requests.post(url, data={'grant_type': 'client_credentials'}, auth=(client_id, client_secret))
#headers curl --header "Authorization: Bearer <access_token>" <GRAPHQL API URL>
url = 'https://fr.warcraftlogs.com/oauth/token'
data = {'grant_type': 'client_credentials'}
response = requests.post(url, data=data, auth=(client_id, client_secret))
access_token = response.json()['access_token']
headers = {'Authorization': 'Bearer ' + access_token}
requete={}
requete['query'] = "query{characterData{character{name}}}"
response = requests.post('https://www.warcraftlogs.com/api/v2/client', headers=headers, json=requete)
print(response.json())










