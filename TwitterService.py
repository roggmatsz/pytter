import requests

class TwitterService(object):
    def __init__(self, baseUrl, bearerToken):
        self.baseUrl = baseUrl
        self.authorizationHeader = {\
            'Authorization': 'Bearer {}'.format(bearerToken['access_token'])\
        }

    def getUserInfo(self, username='roggmatz', endpoint='/users'):
        userParams = {'usernames': username}
        request = requests.get(\
            self.baseUrl + endpoint,\
            headers=self.authorizationHeader,\
            params=userParams)

        # TODO: Factor out validation block into separate function
        if request.status_code != 200:
            print(request.status_code)
            raise Exception('Something went wrong in the User request.')
        else:
            print(request.json())
        
        return request.json()[0]

    def getTweet(self, tweetId, endpoint='/tweets'):
        params = {'ids': tweetId}
        request = requests.get(\
            self.baseUrl + endpoint,\
            headers=self.authorizationHeader,\
            params=params)
        
        # TODO: Factor out validation block into separate function
        if request.status_code != 200:
            print(request.status_code)
            raise Exception('Something went wrong in the User request.')
        else:
            print(request.json())

        return request.json()

    def getTimeline(self, user_id, count=6):
        timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {'user_id': user_id, 'count': count}
        request = requests.get(\
            timeline_url,\
            headers=self.authorizationHeader,\
            params=params)

        # TODO: Factor out validation block into separate function
        if request.status_code != 200:
            print(request.status_code)
            raise Exception('Something went wrong in the User request.')
        else:
            print(request.json())

        return request.json()
