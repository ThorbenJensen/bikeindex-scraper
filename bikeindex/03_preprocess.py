""" Preprocessing scraped data for modeling. """
# %%
import ast
from typing import List

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


df_select['public_images_thumbs'] = df_select.public_images.apply(public_images_thumbs)
df_select['public_images_count'] = df_select.public_images_thumbs.apply(len)

# %% FILTER ROWS WITH IMAGES
df_filter = df_select.query("public_images_count > 0").reset_index()

# %% TO CSV
df_filter.to_csv("data/df_filter.csv", index=False, sep=";", quotechar="'")

# %%
# TODO: create multiple rows for images with more than one image
