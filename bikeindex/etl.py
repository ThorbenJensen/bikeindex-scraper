""" Functions for ETL operations. """

from typing import List


def id_from_image_link(link: str) -> str:
    """Extracting ID as String from link to thumbnail.
    Arguments:
        link {str} -- Weblink to thumbnail.
    Returns:
        str -- ID of image.
    """
    return link.split("/")[-2]


def thumbs_from_dict_list(dict_list: List[dict]) -> List[str]:
    """Get values for key 'thumbs' in list of dictionaries.
    Arguments:
        dict_list {List[dict]} -- List of dictionaries with key 'thumbs'.
    Returns:
        List[str] -- Values for key 'thumbs'.
    """
    return [e["thumb"] for e in dict_list]
