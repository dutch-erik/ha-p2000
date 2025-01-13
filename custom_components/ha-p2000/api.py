import requests  # Zorg ervoor dat dit correct geïmporteerd is
import json
import logging
_LOGGER = logging.getLogger(__name__)

class P3000Api:
    url = "https://beta.alarmeringdroid.nl/api2/find/"

    def __init__(self):
        self.session = requests.Session()

    def get_data(self, apiFilter):
        try:
            response = self.session.get(self.url + json.dumps(apiFilter),
                                        params={},
                                        allow_redirects=False)

            if response.status_code != 200:
                raise RuntimeError("Request failed: %s", response)

            data = json.loads(response.content.decode('utf-8'))

            if len(data['meldingen']) == 0:
                return None

            # Filter de meldingen op basis van de 'melding' waarde
            melding_filter = apiFilter.get('melding', None)
            if melding_filter:
                # Zoek naar meldingen die de filtertekst bevatten
                filtered_meldingen = [melding for melding in data['meldingen'] if melding_filter in melding.get('melding', '')]
            else:
                filtered_meldingen = data['meldingen']

            if len(filtered_meldingen) == 0:
                return None

            # Neem de eerste gefilterde melding (kan later worden uitgebreid)
            result = filtered_meldingen[0]

            # Rename lat & lon
            result["latitude"] = result.get("lat", None)
            result["longitude"] = result.get("lon", None)

            if 'lat' in result:
                del result['lat']

            if 'lon' in result:
                del result['lon']

            # Return result
            return result

        except requests.exceptions.ConnectTimeout:
            _LOGGER.warning("Connection to %s timed out.", self.url)
            return None
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error fetching data from %s: %s", self.url, e)
            return None
