# %%
import os
import urllib
import time

import pandas as pd

IMG_DIR = "data/download/"

# %% LOAD DATA
df_merged = pd.read_csv("data/df_merged.csv", delimiter=";", quotechar="'").assign()


# %% IMAGE ID
def id_froM_link(link: str) -> str:
    return link.split("/")[-2]


df_merged["thumbnail_id"] = df_merged.thumbnail.apply(id_froM_link)
assert not df_merged.thumbnail_id.duplicated().any(), "Duplicated thumbnail ids!"

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
