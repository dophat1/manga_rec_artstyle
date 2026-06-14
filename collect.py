import PIL
import numpy as np 
import requests
import os
import json
import time
from PIL import Image
from io import BytesIO


BASE_URL = "https://api.mangadex.org"

def get_manga_id(title):
    
    r = requests.get(
        f"{BASE_URL}/manga",
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

"""
1. Make the HTTP request with the manga UUID
2. Parse the JSON response
3. Check if empty → raise error
4. Extract full list of chapter IDs
5. Evenly space sample down to N chapters
6. Return sampled chapter IDs
"""

def get_chapter_ids(manga_id: str, n_samples: int = 10) -> list[str]:
    """Fetch all chapter IDs for a manga, evenly sampled down to n_samples."""
    chapter_ids = []
    offset = 0
    limit = 100  # max allowed by MangaDex

    while True:
        r = requests.get(
            f"{BASE_URL}/manga/{manga_id}/feed",
            params={
                "limit": limit,
                "offset": offset,
                "translatedLanguage[]": "en",   # remove if you want all languages
                "order[chapter]": "asc",
            },
        )
        r.raise_for_status()
        payload = r.json()

        chapter_ids.extend(ch["id"] for ch in payload["data"])

        offset += limit
        time.sleep(0.5)
        if offset >= payload["total"]:
            break

    if not chapter_ids:
        raise ValueError(f"No chapters found for manga {manga_id}")

    # Evenly spaced sample down to n_samples
    if len(chapter_ids) <= n_samples:
        return chapter_ids
    step = (len(chapter_ids) - 1) / (n_samples - 1)
    return [chapter_ids[round(i * step)] for i in range(n_samples)]


"""
1.Make the HTTP request with the chapter ID
2.Parse the JSON response
3.Check if empty → raise error
4.Extract full list of page image URLs
5.Return the selected image URLs

"""
def get_panel_urls(chapter_id):
    r = requests.get(
        f"{BASE_URL}/at-home/server/{chapter_id}"
    )
    chapter_url = r.json()
    if len(chapter_url["chapter"]["data"]) == 0:
        raise ValueError("No pages found")
    
    chapter_hash = chapter_url["chapter"]["hash"]

    urls = [ f"{chapter_url["baseUrl"]}/data/{chapter_hash}/{url}" for url in chapter_url["chapter"]["data"]]

    return urls

def filter_panels(url):

    try:
        image = Image.open(BytesIO(requests.get(url).content))
    except:
        return False
    
    
    pixels = np.array(image)
    channel_means = pixels.mean(axis=(0, 1))
    
    
    # Check for blank panels
    if np.var(pixels) < 500:
        return False
    
    # Check for too max text
    elif np.mean(pixels) > 200:
        return False
    
    # Check for color pages
    elif  np.var(channel_means) > 500: # mean of each channel → 3 numbers
        return False
    
    # Passed case
    else:
        return True

def main(titles):
    
    for title in titles:
        all_panels = []
        manga_id = get_manga_id(title)
        chapter_id = get_chapter_ids(manga_id)
        os.makedirs(f"dataset/{title}", exist_ok=True)
        for panel in chapter_id:
            panel_urls = get_panel_urls(panel)
            for panel_url in panel_urls:
                checked_panel = filter_panels(panel_url)
                if checked_panel == True:
                    all_panels.append(panel_url)
        
        panel_number = 0 
        for panel_url in all_panels:
            image = Image.open(BytesIO(requests.get(panel_url).content))
            image.save(f"dataset/{title}/panel_{panel_number:03d}.jpg")
            panel_number += 1
    
    print("Successfully saved all panels")

id = get_manga_id('Shitsurakue')
url = get_panel_urls('56c214e7-3fb7-44d9-8f05-106c9959ba59')
print(url)
