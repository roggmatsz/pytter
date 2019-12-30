import base64
import requests

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