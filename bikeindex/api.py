""" Functions that wrap API. """

import json

import requests

URL_BIKES: str = "https://bikeindex.org:443/api/v3/bikes/"


def get_bike(bike_id: int) -> dict:
    response = requests.get(URL_BIKES + str(bike_id))
    result = json.loads(response.text)
    return result


def search_all(page: int, per_page: int = 100) -> requests.models.Response:
    url_search = "https://bikeindex.org:443/api/v3/search"
    response = requests.get(
        url_search,
        params={"page": page, "per_page": per_page, "query": "e", "stolenness": "all"},
    )
    return response
