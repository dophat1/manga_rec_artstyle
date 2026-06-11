import PIL
import numpy as np 
import requests
import os

def get_manga_id(title):
    
    base_url = "https://api.mangadex.org"

    r = requests.get(
        f"{base_url}/manga",
        params={"title": title}
    )

    if r.status_code == 200:
        manga_id = [manga["id"] for manga in r.json()["data"]]
        if len(manga_id) == 0:
            raise ValueError("No result found")
        
        else:
            result = manga_id[0]
            return result
    
    else:
        raise ValueError(f"There is no manga name {title}")


def get_chapter_ids(manga_id): 
    pass 