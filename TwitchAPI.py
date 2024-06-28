import requests

#Twich API handler, dont touch

class TwitchAPI:
    def __init__(self, client_id, client_secret):
        #Twitch API Stuff----------------------------------
        self.client_id = client_id
        self.client_secret = client_secret

        #Get OAuth Token
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        auth_response = requests.post(auth_url, params=auth_params)
        self.auth_data = auth_response.json()
        access_token = self.auth_data['access_token']
        #------------------------------------------------

    def queryViewers(self, streamName):
        streamer_name = streamName
        access_token = self.auth_data['access_token']
        
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {access_token}'
        }

        url = 'https://api.twitch.tv/helix/streams'
        params = {
            'user_login': streamer_name
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        #Get the Viewer Count
        if data['data']:
            viewer_count = data['data'][0]['viewer_count']
            print(f"Viewer Count for {streamer_name}: {viewer_count}")
            return viewer_count
        else:
            print(f"{streamer_name} is not currently live")

    

        