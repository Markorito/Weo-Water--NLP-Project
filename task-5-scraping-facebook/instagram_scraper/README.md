# 1. sub-task: Scraping Instagram with Graph API

With Python

## Useful documentation:

[Official documentation](https://developers.facebook.com/docs/instagram-api/)

## Instagram Graph API limitations:

* Only returns public photos and videos.
* Only returns media objects published within 24 hours of query execution.
* Will not return promoted/boosted/ads media.
* Responses are paginated with a maximum limit of 50 results per page.
* Responses will not always be in chronological order.
* You can query a maximum of 30 unique hashtags within a 7 day period.
* You cannot request the username field on returned media objects.
* Responses will not include any personally identifiable information.
* This endpoint only returns an after cursor for paginated results; a before cursor will not be included. In addition, the after cursor value will always be the same for each page, but it can still be used to get the next page of results in the result set.

## Requirements:

* Facebook account
* Instagram business/creator account - [Set Up a Business Account on Instagram](https://help.instagram.com/502981923235522/robots.txt)
* A Facebook page

## Required steps to run the code:

1. Create an app on [Facebook for Developers](https://developers.facebook.com/) Log In > My Apps > Create App
2. From the left side menu click on "Products **+**" > **Facebook Login** Set Up
3. **Facebook Login** > Settings > insert a Valid OAuth Redirect URIs (any site is good). FYI this is the URI that Facebook will redirect the user back after they log in (sometimes there are some TOUs to agree on)
4. From the toolbar: Tools > _choose the desired app_
5. From the drop-down menu under **Facebook App** and select your app
6. Click on **Generate Access Token**
7. Add the following permission: _Instagram_basic, Instagram_manage_comments, Instagram_manage_insights, instagram_content_publish, pages_read_engagement, pages_manage_posts_
8. Click (again) on **Generate Access Token**

## Where to find all the IDs needed for the _scraper_agent_
* **Access_token** = see above
*  **client_id** = From the hompage of your app: Settings > App ID
*  **client_SECRET** = From the hompage of your app: Settings > App Secret > insert your password
*  **graph_domain** and **graph_version** = are already set

## How to run setup.py
The script "setup.py" scrapes the data related to specific hashtags in the last 24 hours.
In order to run the script, we need to update the access_token used to initialize the scraping agents.
There are two scraping agents because it was needed to work around the limitations posed by the TOU.

The data scraped are collected in some csv files that have the date and hashtag on their name.

# 2. data_tagger.py 
Data tagger is a script to manually tag the data scraped by the scraping agent. (In order to make the script work you need an Instagram account).

!!! It doesn't work already on IUNIX systems, just on windows.
## How it works?
The script reads the csv files (inside the specified folder "dir") row by row. For each post (row) it opens a brwoser page (default browser "microsoft edge") using he permalink related to the post. 
Every time a page is opened, the script asks the user, via terminal, if the post is useful or not.
All the useful post are saved in the "output_cleaned" folder

## How to run data_tagger.py

1. copy the subfolders that you want to clean from ```../output_to_clean/[...]``` to ```../tmp_output_to_clean/```.
2. run the command:
```
python data_tagger.py [browser]
```
To value of ```browser``` is optional. If no browser is chosen it will open Ms Edge. (for now the only values accepted are ```msedge``` and ```mschrome```).

Otherwise, you can run it from any IDE. In this case, unless you don't change the IDE's setting or code, msedge will be chosen as browser.


If encoutner any problem, you can move the full path WeoWater/task-5.../.../ on google drive and use the notebook version of the data tagger. This version will work in any OS (it has been tested on Chrome, Brave and Edge browsers). Before starting, ensure there are no javascript or popups blocker.




