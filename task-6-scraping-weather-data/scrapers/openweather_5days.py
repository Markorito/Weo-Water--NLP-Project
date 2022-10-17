def OpenWeatherMap_5days(location_name=None, longitude=None, latitude=None, units='metric'):
    #import packages
    import requests
    import datetime as dt
    import time
    import geopy
    from geopy.geocoders import Nominatim
    import numpy as np
    import pandas as pd

    #determine latitiude and longitude based on what was passed to function (may change from what was )
    if location_name:
        locator = Nominatim(user_agent='myGeocoder')
        location = locator.geocode(location_name)
        lati = str(location.latitude)
        long = str(location.longitude)
    else: 
        lati = str(latitude)
        long = str(longitude)
    
    exclude='current,minutely,hourly'
    
    #define API key
    API_key = '617dec18b0669db53a5ab299c4e48609'
    
    output = pd.DataFrame()
    
    for i in range(0,6):
        #datetime = dt.datetime.strptime(date, '%m/%d/%Y')
        date = dt.date.today()-dt.timedelta(days=i)
        datetimeunix = int(time.mktime(date.timetuple()))
    
        #One Call: Current weather, Minute forecast for 1 hour, Hourly forecast for 48 hours, Daily forecast for 7 days
        #National weather alerts, Historical weather data for the previous 5 days
        url = r'''https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={API_key}'''.format(lat=lati, lon=long, API_key=API_key, time=datetimeunix)
    
        response = requests.get(url)
        scraped = response.json()
        
        hourly=pd.DataFrame(scraped['hourly'])

        hourly_1 = pd.concat([hourly.drop(['weather'], axis=1), hourly['weather'].apply(lambda x: pd.Series(x[0]))], axis=1)
        hourly_drop = ['feels_like','pressure', 'visibility','humidity','dew_point','clouds','wind_speed', 'wind_gust', 'wind_deg','id','icon']
        for col in hourly_drop:
            if col in hourly_1.columns:
                hourly_1.drop(columns=[col], inplace=True)
        hourly_1['dt'] = pd.to_datetime(hourly_1['dt'], unit='s')
        if 'rain' not in hourly_1.columns:
            hourly_1['rain']=0
        if 'snow' not in hourly_1.columns:
            hourly_1['snow']=0
        hourly_1.insert(1, value=scraped['lat'], column='latitude')
        hourly_1.insert(1, value=scraped['lon'], column='longitude')
        hourly_1.rename(columns={'dt':'date', 'main':'weather_short','description':'weather_long'}, inplace=True)
                
        if i==0:
            output = hourly_1
        else:
            output = pd.concat([output,hourly_1])
        
    #add prefix for specific scraper
    output = output.add_prefix('owm_')
    #correct date column to date for mathcing with others
    output.rename(columns={'owm_date':'date'}, inplace=True)
        
    return output
    
    
