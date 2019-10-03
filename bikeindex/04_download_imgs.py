# %%
import os
import urllib
import time

import pandas as pd

IMG_DIR = "data/download/"

# %% LOAD DATA
df_merged = pd.read_csv("data/df_merged.csv", delimiter=";", quotechar="'") \
    .assign()


# %% IMAGE ID
def id_froM_link(link: str) -> str:
    return link.split("/")[-2]


df_merged["thumbnail_id"] = df_merged.thumbnail.apply(id_froM_link)
assert not df_merged.thumbnail_id.duplicated().any(), "Duplicated thumbnail ids!"

# %% DOWNLOAD ALL IMAGES
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

for link, id in zip(df_merged.thumbnail, df_merged.thumbnail_id):
    print(f"downloading image {id}.jpg "
          f"from {link} "
          f"({(df_merged.thumbnail_id==id).idxmax() + 1}/{len(df_merged)})...")
    urllib.request.urlretrieve(link, IMG_DIR + id + ".jpg")
    time.sleep(2)

# %%
