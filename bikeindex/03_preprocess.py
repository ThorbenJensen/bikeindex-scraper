""" Preprocessing scraped data for modeling. """
# %%
import ast
from typing import List, Tuple

import pandas as pd

# %% LOAD IDs
df_bikes = pd.read_csv("data/df_bikes.csv", sep=";", quotechar="'")

df_bikes.columns

# %%
df_select = df_bikes.filter(
    items=[
        # basic info
        "id",
        "type_of_cycle",
        "year",
        # manufacturer
        "manufacturer_id",
        "manufacturer_name",
        # frame
        "frame_colors",
        "frame_model",
        "frame_size",
        "frame_material_slug",
        # wheels
        "rear_wheel_size_iso_bsd",
        "front_wheel_size_iso_bsd",
        "rear_tire_narrow",
        "front_tire_narrow",
        "front_gear_type_slug",
        "rear_gear_type_slug",
        # images
        "is_stock_img",
        "public_images",
    ]
)


# %% RE-STRUCTURE 'PUBLIC IMAGES'
def public_images_thumbs(images_json: str) -> List[str]:
    images_list: List[dict] = ast.literal_eval(images_json)
    thumbs_list: List[str] = [i["thumb"] for i in images_list]
    return thumbs_list


df_select["public_images_thumbs"] = df_select.public_images.apply(public_images_thumbs)
df_select["public_images_count"] = df_select.public_images_thumbs.apply(len)

# %% FILTER ROWS WITH IMAGES
df_filter = df_select.query("public_images_count > 0").reset_index()

# %% make numbers unique per row

# get tuples of IDs and thumb links
id_thumb: List[Tuple[int, str]] = []
for _, row in df_filter.iterrows():
    id: int = row.id
    thumbs: List[str] = row.public_images_thumbs
    for thumb in thumbs:
        id_thumb.append((id, thumb))
df_id_thumb = pd.DataFrame(data=id_thumb, columns=["id", "thumbnail"])

# join new columns to dataframe, drop obsolete ones
df_merged = pd.merge(
    left=df_id_thumb, right=df_filter, how="inner", left_on="id", right_on="id"
).drop(
    columns=["index", "public_images", "public_images_thumbs", "public_images_count"]
)
assert len(df_merged) == len(df_id_thumb), "Lines got lost at merge."

# %% TO CSV
df_merged.to_csv("data/df_merged.csv", index=False, sep=";", quotechar="'")

# %%
