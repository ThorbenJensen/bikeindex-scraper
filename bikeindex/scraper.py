""" Scrape bike information from api. """
# %%
import json
import math
import time

import pandas as pd
import requests

URL_BIKES: str = "https://bikeindex.org:443/api/v3/bikes/"
MAX_ID: int = 6059692
PATH_DOWNLOAD: str = "data/download/"
PER_PAGE = 100


def get_bike(bike_id: int) -> dict:
    response = requests.get(URL_BIKES + str(bike_id))
    result = json.loads(response.text)
    return result


def save_dict_as_json(result: dict, file_path: str):
    with open(file_path, "w") as outfile:
        json.dump(result, outfile, indent=4)


def search_all(page: int, per_page: int = PER_PAGE) -> requests.models.Response:
    url_search = "https://bikeindex.org:443/api/v3/search"
    response = requests.get(
        url_search,
        params={"page": page, "per_page": per_page, "query": "e", "stolenness": "all"},
    )
    return response


# %% Scrape all bikes
response = search_all(page=1, per_page=PER_PAGE)
total: int = int(response.headers["total"])
page_max = math.ceil(total / PER_PAGE)
pages = list(range(1, page_max + 1))

bikes_all = []

for page in pages:
    print(f"Iterating over page {page} of {page_max}...")
    response = search_all(page=page)
    bikes = response.json()["bikes"]
    bikes_all.extend(bikes)
    time.sleep(10)

# %% To DataFrame
df = pd.DataFrame(bikes_all)
df.head()
df.to_csv("data/bikes.csv")

# %%
