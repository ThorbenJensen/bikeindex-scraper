#!/usr/bin/env python3
""" Scrape bike information from API. """
# %%
import math
import time

import pandas as pd

from bikeindex.api import search_all

MAX_ID: int = 6059692
PATH_DOWNLOAD: str = "data/download/"
PER_PAGE = 100


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
df.to_csv("data/bikes.csv", sep=";", quotechar="'", index=False)

# %%
