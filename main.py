import yaml
import requests
import base64

# bearer / application only auth is used to access read-only data
# oauth 1.0a is needed to do POST-ey stuff

class TwitterAuth:
    def __init__(self, url, secrets, existingToken=None):
        self.url = url
        self.existingToken = existingToken
        self.secrets = secrets
        self.concatenatedKey = None

    def getAuthToken(self):
        if self.existingToken is not None:
            print('Found existing token: {}'.format(self.existingToken))
            pass
        
        # make concatKeys
        self.concatenatedKey = base64.urlsafe_b64encode('{}:{}'.format(\
            self.secrets['key'], self.secrets['secret']).encode('ascii'))\
            .decode('ascii')

        # make request header
        auth_header = {\
            'Authorization': 'Basic {}'.format(self.concatenatedKey),\
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'\
        }
        data = 'grant_type=client_credentials'
        
        # send the request and do code validation
        request = requests.post(self.url, headers=auth_header, data=data)
        if request.status_code != 200:
            print(request.status_code)
        else:
            print(request.json())
            self.existingToken = request.json()
            return self.existingToken

def readYaml():
    with open('config.yaml') as f:
        return yaml.safe_load(f)

def makeHeaders(keys):
    return {'Authorization': 'Basic {}'.format(keys), 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

def makePostAuthHeaders(token):
    return {'Authorization' : 'Bearer {}'.format(token['access_token'])}

def makeOAuthHeaders():
    return {'Authorization': 'OAuth oauth_consumer_key={}, oauth_token={}, oauth_token_secret={}, oauth_version="1.0'}

if __name__ == '__main__':
    DO_THIS = False

    session_token = {'token_type': 'bearer', 'access_token': 'AAAAAAAAAAAAAAAAAAAAAL5FBAEAAAAAqoth5%2B6cM2dCT78zx%2BAJWAfPI%2FA%3DesoJlBaxUcW0bnSdOGjyG8dcZZOKf6dC4qWEAyYJvYIPylWGl5'}

    config = readYaml()
    data = 'grant_type=client_credentials'
    concat_keys = base64.urlsafe_b64encode('{}:{}'.format(config['consumer_key'], config['consumer_secret']).encode('ascii')).decode('ascii')

    if session_token == None:
        request = requests.post(config['token_url'], headers=makeHeaders(concat_keys), data=data)
        print(request.json())

    #if DO_THIS:
        # get basic information for my twitter account
    params = { 'usernames': 'roggmatz'}
    userRequest = requests.get(\
        config['users_url'],\
        headers={'Authorization': 'Bearer {}'.format(session_token['access_token'])},\
        params=params\
    ).json()['data']

    if DO_THIS:
        # get most recent tweet from basic user info
        twitter_id = userRequest[0]['most_recent_tweet_id']
        tweetsRequest = requests.get(config['tweets_url'],\
            headers=makePostAuthHeaders(session_token),\
            params={'ids': twitter_id})

    # get user timeline tweets
    allTweetsRequest = requests.get(config['timeline_url'],\
        headers=makePostAuthHeaders(session_token),\
        params={'user_id': userRequest[0]['id'], 'count': 3})

