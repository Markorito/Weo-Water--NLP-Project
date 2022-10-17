from cliff.api import Cliff

class Results:
    """Results returned by the geoparser."""
    def __init__(self, results):
        # Raise and exception if CLIFF returns an error
        if results['status'] == 'error':
            raise ValueError('CLIFF geoparsing failed: {}'.format(
                results['details']))
        self.results = results

    def get_countries(self):
        """
        Return the countries most mentioned in the text.

        This tries to guess the countries that the text is about. It will not
        give all countries in the text, see `get_locations` instead.

        # Example

        >>> geo = GeoParser('http://localhost:8080')
        >>> results = geo.parse_text('Is this text about India or China. What if I mention Shanghai?')
        >>> pprint(results.get_countries())
        [{'countryCode': 'CN',
          'countryGeoNameId': '1814991',
          'featureClass': 'A',
          'featureCode': 'PCLI',
          'id': 1814991,
          'lat': 35.0,
          'lon': 105.0,
          'name': 'People’s Republic of China',
          'population': 1392730000,
          'score': 2,
          'stateCode': '00',
          'stateGeoNameId': ''}]
        """
        assert self.results['status'] == 'ok'
        focus = self.results["results"]["places"]["focus"]
        countries = focus.get("countries", [])
        return countries

    def get_cities(self):
        """
        Return the cities most mentioned in the text.

        This tries to guess the cities that the text is about. It will not
        give all cities in the text, see `get_locations` instead.

        # Example

        >>> geo = GeoParser('http://localhost:8080')
        >>> results = geo.parse_text('Is this text about India or China. What if I mention Shanghai?')
        >>> pprint(results.get_cities())
        [{'countryCode': 'CN',
          'countryGeoNameId': '1814991',
          'featureClass': 'P',
          'featureCode': 'PPLA',
          'id': 1796236,
          'lat': 31.22222,
          'lon': 121.45806,
          'name': 'Shanghai',
          'population': 22315474,
          'score': 1,
          'stateCode': '23',
          'stateGeoNameId': '1796231'}]
        """
        assert self.results['status'] == 'ok'
        focus = self.results["results"]["places"]["focus"]
        cities = focus.get("cities", [])
        return cities

    def get_states(self):
        """
        Return the states (admin-1) most mentioned in the text.

        This tries to guess the states that the text is about. It will not
        give all states in the text, see `get_locations` instead.

        # Example

        >>> geo = GeoParser('http://localhost:8080')
        >>> results = geo.parse_text('Is this text about India or China. What if I mention Shanghai?')
        >>> pprint(results.get_states())
        [{'countryCode': 'CN',
          'countryGeoNameId': '1814991',
          'featureClass': 'A',
          'featureCode': 'ADM1',
          'id': 1796231,
          'lat': 31.16667,
          'lon': 121.41667,
          'name': 'Shanghai Shi',
          'population': 18880000,
          'score': 1,
          'stateCode': '23',
          'stateGeoNameId': '1796231'}]
        """
        assert self.results['status'] == 'ok'
        focus = self.results["results"]["places"]["focus"]
        states = focus.get("states", [])
        return states

    def get_locations(self):
        """
        Return all locations mentioned in the text.

        # Example

        >>> geo = GeoParser('http://localhost:8080')
        >>> results = geo.parse_text('Is this text about India or China?')
        >>> pprint(results.get_locations())
        [{'confidence': 1.0,
          'countryCode': 'IN',
          'countryGeoNameId': '1269750',
          'featureClass': 'A',
          'featureCode': 'PCLI',
          'id': 1269750,
          'lat': 22.0,
          'lon': 79.0,
          'name': 'Republic of India',
          'population': 1352617328,
          'source': {'charIndex': 19, 'string': 'India'},
          'stateCode': '00',
          'stateGeoNameId': ''},
         {'confidence': 1.0,
          'countryCode': 'CN',
          'countryGeoNameId': '1814991',
          'featureClass': 'A',
          'featureCode': 'PCLI',
          'id': 1814991,
          'lat': 35.0,
          'lon': 105.0,
          'name': 'People’s Republic of China',
          'population': 1392730000,
          'source': {'charIndex': 28, 'string': 'China'},
          'stateCode': '00',
          'stateGeoNameId': ''}]
        """
        assert self.results['status'] == 'ok'
        locations = self.results["results"]["places"]["mentions"]
        return locations

class GeoParser():
    """
    Geoparser for finding geographical locations in text.

    This requires a CLIFF server running in the background. For example, use the
    following Docker commands to run the server:

        docker pull rahulbot/cliff-clavin
        docker run -p 8080:8080 -m 8G -d rahulbot/cliff-clavin

    Then the server will be accessible under the following URL:

        http://localhost:8080
    """

    def __init__(self, server_url):
        """
        Initialize the geoparser.

        **Arguments:**
        `server_url`: URL to the CLIFF server (including port).
        """
        self.cliff = Cliff(server_url)

    def parse_text(self, text, clean_hashtags=True, demonyms=False,
                   language='EN'):
        """
        Geoparse the given text.

        **Arguments:**
        `text`: The text to be parsed.
        `clean_hashtags`: Whether hashtags should be cleaned by removing `#`.
        `demonyms`: Whether demonyms should be detected (can be slow).
        `language`: The language of the text.

        **Returns:** The results from parsing the text (see `Results`).
        """
        if clean_hashtags:
            text = text.replace('#', '')
        return Results(self.cliff.parse_text(text, demonyms=demonyms,
                                             language=language))

if __name__ == '__main__':
    from pprint import pprint

    # Make sure to run a CLIFF server on localhost, port 8080.
    geo = GeoParser('http://localhost:8080')
    results = geo.parse_text('Is this text about India or China? What if I mention Shanghai?')

    print('Most mentioned countries:')
    pprint(results.get_countries())
    print('\nMost mentioned states (admin-1):')
    pprint(results.get_states())
    print('\nMost mentioned cities:')
    pprint(results.get_cities())
    print('\nAll mentioned locations:')
    pprint(results.get_locations())
