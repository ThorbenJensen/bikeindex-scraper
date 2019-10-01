# %%
import sys
import time

import pandas as pd

sys.path.append(".")
from bikeindex.api import get_bike


# %% LOAD IDs
df = pd.read_csv("data/bikes.csv", sep=";", quotechar="'")
assert not df.id.duplicated().any(), "duplicated IDs in bikes.csv"

# %% SCRAPE BIKES
# ids of bikes
bike_ids = sorted(list(df.id.values))
len(bike_ids)

# scrape dictionaries of bike records
bikes = []
for bike_id in bike_ids:
    print(
        f"Scraping bike with ID {bike_id} "
        f"({bike_ids.index(bike_id) + 1}/{len(bike_ids)})..."
    )
    bike_dict = get_bike(bike_id)["bike"]
    bikes.append(bike_dict)
    time.sleep(2)

# %% SAVE TO DATAFRAME
df_bikes = pd.DataFrame(bikes)
df_bikes.to_csv("data/df_bikes.csv", sep=";", quotechar="'", index=False)

# %%
