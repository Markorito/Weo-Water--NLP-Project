import requests
import json
import pandas as pd

class Instagram_agent:
    """
    This agent uses the Official Instagram Graph API to get:
     - Info about hashtags
     - get content from most recent post related to an hashtag
     - get content from top trending post related to an hashtag
     - get top trending hashtags
    """

    def __init__(
        self,
        access_token,
        client_id,
        client_secret,
        graph_domain="https://graph.facebook.com/",
        graph_version="v10.0",
        debug="no",
    ) -> None:
        self.access_token = access_token  # access token for use with all api calls
        self.client_id = client_id  # client id from facebook app IG Graph API Test
        self.client_secret = client_secret  # client secret from facebook app
        self.graph_domain = graph_domain  # base domain for api calls
        self.graph_version = graph_version  # version of the api we are hitting
        self.endpoint_base = (
            self.graph_domain + self.graph_version + "/"
        )  # base endpoint with domain and version
        self.debug = debug

        page_info = self.__getUserPage()
        assert (
            "data" in page_info["json_data"]
        ), f'Something went wrong: {page_info["json_data"]["error"]}'

        self.page_id = page_info["json_data"]["data"][0]["id"]  # users page id

        account_info = self.__getInstagramAccount()
        self.instagram_account_id = account_info["json_data"][
            "instagram_business_account"
        ][
            "id"
        ]  # users instagram account id

    def __getUserPage(self):
        """Get facebook pages for a user

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}

        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams["access_token"] = self.access_token  # access token

        url = self.endpoint_base + "me/accounts"  # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug)  # make the api call

    def __getInstagramAccount(self):
        """Get instagram account

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account

        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams[
            "access_token"
        ] = self.access_token  # tell facebook we want to exchange token
        endpointParams["fields"] = "instagram_business_account"  # access token

        url = self.endpoint_base + self.page_id  # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug)  # make the api call

    def makeApiCall(self, url, endpointParams, type):
        """Request data from endpoint with params

        Args:
            url: string of the url endpoint to make request from
            endpointParams: dictionary keyed by the names of the url parameters
        Returns:
            object: data from the endpoint
        """

        if type == "POST":  # post request
            data = requests.post(url, endpointParams)
        else:  # get request
            data = requests.get(url, endpointParams)

        response = dict()  # hold response info
        response["url"] = url  # url we are hitting
        response["endpoint_params"] = endpointParams  # parameters for the endpoint
        response["endpoint_params_pretty"] = json.dumps(
            endpointParams, indent=4
        )  # pretty print for cli
        response["json_data"] = json.loads(
            data.content
        )  # response data from the api -> data.content is the content of the request we carry out
        response["json_data_pretty"] = json.dumps(
            response["json_data"], indent=4
        )  # pretty print for cli

        return response  # get and return content

    def getHashtagInfo(self, hashtag_name):
        """Get info on a hashtag

        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
        Returns:
            object: data from the endpoint
        """

        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams["user_id"] = self.instagram_account_id  # user id making request
        endpointParams["q"] = hashtag_name  # hashtag name
        endpointParams["fields"] = "id,name"  # fields to get back
        endpointParams["access_token"] = self.access_token  # access token

        url = self.endpoint_base + "ig_hashtag_search"  # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug)  # make the api call

    def getHashtagMedia(self, hashtag_id, type):
        """Get posts for a hashtag

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

        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams["user_id"] = self.instagram_account_id  # user id making request
        endpointParams[
            "fields"
        ] = "id,children,date,caption,comments_count,like_count,media_type,media_url,permalink,timestamp "  # fields to get back
        # children -> if it is a post with multiple pictures
        endpointParams["access_token"] = self.access_token  # access token

        url = self.endpoint_base + hashtag_id + "/" + type  # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug)  # make the api call

    def getAtLeastNMediaFromHashtag(self, hashtag_name, min_items=30) -> pd.DataFrame:
        """
        Results form the IG API might be paginated. Here we loop though the pages until we have enough items
        """
        # get the IG hashtag for this location
        hashtag_id = self.getHashtagInfo(hashtag_name)["json_data"]
        if not "data" in hashtag_id:
            raise IOError("Instagram scraper: Reached limit of 30 hash tags per week")
        hashtag_id = hashtag_id["data"][0]["id"]

        # get content for this hashtag
        recent_media = self.getHashtagMedia(hashtag_id, "recent_media")
        content = recent_media["json_data"]["data"]

        # The API limits the number of items returned on a single call,
        # if we want more we need to look at the next page
        next_page = recent_media["json_data"]["paging"]["next"]
        while len(content) < min_items and next_page is not None:
            print(f"so far we have {len(content)}, looking at next page")
            r = requests.get(next_page)
            recent_media = json.loads(r.content)
            print("recent_media keys", recent_media.keys())
            content.extend(recent_media["data"])
            next_page = recent_media["paging"]["next"]

        print(len(content))
        return pd.DataFrame(content)

    def getRecentlySearchedHashtags(self):
        """Get hashtags a user has recently search for

        API Endpoints:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/recently_searched_hashtags?fields={fields}
        Returns:
            object: data from the endpoint
        """

        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams["fields"] = "id,name"  # fields to get back
        endpointParams["access_token"] = self.access_token  # access token

        url = (
            self.endpoint_base
            + self.instagram_account_id
            + "/"
            + "recently_searched_hashtags"
        )  # endpoint url

        return self.makeApiCall(url, endpointParams, self.debug)  # make the api call


def charCorrector(word: str):
    char_dict = {
        "ã¼": "ü",
        "åº": "ź",
        "ã¢": "â",
        "ãº": "ú",
        "ã²": "ò",
        "ä±": "ı",
        "åÿ": "ş",
        "ã³": "ó",
        "ã¨": "è",
        "ã¡": "á",
        "ã©": "é",
        "ãÿ": "ß",
        "ã¿": "ÿ",
        "ã±": "ñ",
        "ã§": "ç",
        "ã¬": "ì",
        "ã«": "ë",
        "ã£": "ã",
        "ã¦": "æ",
        "ã°": "ð",
        "ã¶": "ö",
        "ã¥ã": "å",
        "ãµ": "õ",
        "ã´": "ô",
        "ã»": "û",
        "ã½": "ý",
        "ãª": "ê",
        "ã®": "î",
        "ã¾": "þ",
        "ã¸": "ø",
        "ã¤": "ä",
        "ã¹": "ù",
        "ã¯": "ï",
    }
    # print(f'word: {word}')
    res = word
    for k, v in char_dict.items():
        if word.find(k) != -1:
            # print(f'key {k}')
            # print(f'value {v}')
            res = word.replace(k, v)
            res = charCorrector(res)  # recursive solution to find all the occurrences
            break
    # print(f"result {res}")
    return res


def read_json(file_path):
    with open(file_path) as f:
        data = json.load(f)

    encoded_data = {}
    for k in data.keys():
        encoded_data.update({k: []})
        for v in data[k]:
            encoded_data[k].append(charCorrector(v.lower()))
    return encoded_data


IG_HASHTAGS = dict(
    flood=[
        "inundacion",
        "inundations",
        "selyüzünden",
        "inundación",
        "inundaçao",
        "inondation",
        "inundações",
        "inundaciones",
        "bumabaha",
        "flood",
        "powódź",
        "pagbaha",
        "inundacao",
        "selsuyu",
        "inundation",
        "overstroming",
        "taşkınoldu",
        "alluvione",
        "Überschwemmung",
        "sel suyunun",
        "floods",
        "powodzie",
        "inundar",
        "inondazione",
        "su baskını",
        "flooded",
        "flooding",
        "sutaşkın",
        "Flut",
        "Hochwasser",
        "banjir",
        "inundacão",
        "inonder",
        "inundated",
        "sel bastı",
        "inundação",
        "baha",
        "flashflood",
        "floodwatch",
        "floodwarning",
        "floodwaters",
        "floodseason",
        "flud",
    ],
    drought=["drought", "desiccation", "droughtseason", "desertification"],
)
