""" Preprocessing scraped bike data for modeling. """
# %%
from ast import literal_eval
from typing import List, Tuple

import pandas as pd

# %% LOAD BIKE DATA
df_bikes = pd.read_csv("data/df_bikes.csv", sep=";", quotechar="'")

df_select = df_bikes.filter(
    items=(
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
    )
)


# %% GET LINKS TO THUMBNAIL IMAGES
def thumbs_from_dict_list(dict_list: List[dict]) -> List[str]:
    """Get values for key 'thumbs' in list of dictionaries.
    Arguments:
        dict_list {List[dict]} -- List of dictionaries with key 'thumbs'.
    Returns:
        List[str] -- Values for key 'thumbs'.
    """
    return [e["thumb"] for e in dict_list]


df_select["public_images_thumbs"] = df_select.public_images.map(literal_eval).map(
    thumbs_from_dict_list
)
df_select["public_images_count"] = df_select.public_images_thumbs.map(len)

# %% FILTER ROWS WITH AT LEAST ONE IMAGE
df_filter = (
    df_select.query("public_images_count > 0")
    .reset_index()
    .drop(columns=["public_images", "public_images_count"])  # columns now obsolete
)

# %% make numbers unique per row

# get tuples of IDs and thumb links
id_thumb: List[Tuple[int, str]] = [
    (row.id, thumb)
    for _, row in df_filter.iterrows()
    for thumb in row.public_images_thumbs
]
df_id_thumb = pd.DataFrame(data=id_thumb, columns=["id", "thumbnail"])

# join new columns to dataframe, drop obsolete ones
df_merged = pd.merge(
    left=df_id_thumb, right=df_filter, how="inner", left_on="id", right_on="id"
).drop(columns=["public_images_thumbs"])  # column now obsolete

assert len(df_merged) == len(df_id_thumb), "Lines got lost at merge."


# %% Create unique ID for images
def id_from_image_link(link: str) -> str:
    """Extracting ID as String from link to thumbnail.
    Arguments:
        link {str} -- Weblink to thumbnail.
    Returns:
        str -- ID of image.
    """
    return link.split("/")[-2]


df_merged["thumbnail_id"] = df_merged.thumbnail.map(id_from_image_link)

assert not df_merged.thumbnail_id.duplicated().any(), "Duplicated thumbnail ids!"


# %% SAVE TO CSV
df_merged.to_csv("data/df_merged.csv", index=False, sep=";", quotechar="'")

# %%
