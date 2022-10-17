import requests
import json

class Scraping_agent:
    """
    This agent uses the Official Instagram Graph API to get:
     - Info about hashtags
     - get content from most recent post related to an hashtag
     - get content from top trending post related to an hashtag
     - get top trending hashtags 
    """

    def __init__(self, access_token, client_id,client_secret,graph_domain='https://graph.facebook.com/',graph_version='v10.0',debug='no') -> None:
        self.access_token = access_token        # access token for use with all api calls
        self.client_id = client_id              # client id from facebook app IG Graph API Test
        self.client_secret = client_secret      # client secret from facebook app
        self.graph_domain = graph_domain        # base domain for api calls
        self.graph_version = graph_version      # version of the api we are hitting
        self.endpoint_base = self.graph_domain + self.graph_version + '/'  # base endpoint with domain and version
        self.debug = debug

        page_info = self.__getUserPage()
        self.page_id = page_info['json_data']['data'][0]['id']     # users page id

        account_info =  self.__getInstagramAccount()
        self.instagram_account_id = account_info['json_data']['instagram_business_account']['id']# users instagram account id

    def __getUserPage(self):
        """ Get facebook pages for a user
        
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}

        Returns:
            object: data from the endpoint
        """
        endpointParams = dict() # parameter to send to the endpoint
        endpointParams['access_token'] = self.access_token # access token

        url = self.endpoint_base + 'me/accounts' # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug) # make the api call

    def __getInstagramAccount(self):
        """ Get instagram account

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account

        Returns:
            object: data from the endpoint
        """
        endpointParams = dict() # parameter to send to the endpoint
        endpointParams['access_token'] = self.access_token # tell facebook we want to exchange token
        endpointParams['fields'] = 'instagram_business_account' # access token

        url = self.endpoint_base + self.page_id # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug) # make the api call


    def makeApiCall(self, url, endpointParams, type):
        """ Request data from endpoint with params
        
        Args:
            url: string of the url endpoint to make request from
            endpointParams: dictionary keyed by the names of the url parameters
        Returns:
            object: data from the endpoint
        """

        if type == 'POST' : # post request
            data = requests.post(url, endpointParams)
        else : # get request
            data = requests.get(url, endpointParams)

        response = dict() # hold response info
        response['url'] = url # url we are hitting
        response['endpoint_params'] = endpointParams #parameters for the endpoint
        response['endpoint_params_pretty'] = json.dumps(endpointParams, indent = 4) # pretty print for cli
        response['json_data'] = json.loads(data.content) # response data from the api -> data.content is the content of the request we carry out
        response['json_data_pretty'] = json.dumps(response['json_data'], indent = 4) # pretty print for cli

        return response # get and return content

    def getHashtagInfo(self, hashtag_name) :
        """ Get info on a hashtag

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
        Returns:
            object: data from the endpoint
        """

        endpointParams = dict() # parameter to send to the endpoint
        endpointParams['user_id'] = self.instagram_account_id # user id making request
        endpointParams['q'] = hashtag_name # hashtag name
        endpointParams['fields'] = 'id,name' # fields to get back
        endpointParams['access_token'] = self.access_token # access token

        url = self.endpoint_base + 'ig_hashtag_search' # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug) # make the api call

    def getHashtagMedia(self, hashtag_id, type) :
        """ Get posts for a hashtag

        type:
            - 'top_media'    # set call to get top media for hashtag
            - 'recent_media' # set call to get recent media for hashtag

        'fields' can be found here:
            https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag/top-media#reading

        API Endpoints:
            https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?user_id={user-id}&fields={fields}
            https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_media?user_id={user-id}&fields={fields}
        Returns:
            object: data from the endpoint
        """

        endpointParams = dict() # parameter to send to the endpoint
        endpointParams['user_id'] = self.instagram_account_id # user id making request
        endpointParams['fields'] = 'id,children,date,caption,comments_count,like_count,media_type,media_url,permalink,timestamp ' # fields to get back
        # children -> if it is a post with multiple pictures
        endpointParams['access_token'] = self.access_token # access token

        url = self.endpoint_base + hashtag_id + '/' + type # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug) # make the api call

    def getRecentlySearchedHashtags(self) :
        """ Get hashtags a user has recently search for

        API Endpoints:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/recently_searched_hashtags?fields={fields}
        Returns:
            object: data from the endpoint
        """

        endpointParams = dict() # parameter to send to the endpoint
        endpointParams['fields'] = 'id,name' # fields to get back
        endpointParams['access_token'] = self.access_token # access token

        url = self.endpoint_base + self.instagram_account_id + '/' + 'recently_searched_hashtags' # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug) # make the api call