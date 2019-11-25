# %%
import os
import urllib
import time

import pandas as pd

IMG_DIR = "data/download/"

# %% LOAD DATA
df_merged = pd.read_csv("data/df_merged.csv", delimiter=";", quotechar="'").assign()

# %% DOWNLOAD ALL IMAGES
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

print("Downloading new files...")
for link, id in zip(df_merged.thumbnail, df_merged.thumbnail_id):
    outfile = IMG_DIR + id + ".jpg"
    if not os.path.exists(outfile):
        print(
            f"downloading image {id}.jpg "
            f"from {link} "
            f"({(df_merged.thumbnail_id==id).idxmax() + 1}/{len(df_merged)})..."
        )
        try:
            urllib.request.urlretrieve(link, outfile)
        except urllib.error.HTTPError:
            continue
        time.sleep(2)

# %%
