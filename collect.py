import PIL
import numpy as np 
import requests
import os
import json

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

def get_chapter_ids(manga_id): 
    r = requests.get(
        f"{BASE_URL}/manga/{manga_id}/feed"
    )
    chapter_ids = []
    
    if r.status_code == 200:
        offset = 0 
        limit = r.json()['limit']

        for chapter in range(offset):
            chapter_id = [chapter["id"] for chapter in r.json()['data']]
            offset += limit 
            chapter_ids.append(chapter_id)
            if len(chapter_id) == 0:
                raise ValueError("No chapter ID found")
            else:
                return chapter_id
    else:
        raise ValueError(f"There is no chapters found")

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
        if offset >= payload["total"]:
            break

    if not chapter_ids:
        raise ValueError(f"No chapters found for manga {manga_id}")

    # Evenly spaced sample down to n_samples
    if len(chapter_ids) <= n_samples:
        return chapter_ids
    step = (len(chapter_ids) - 1) / (n_samples - 1)
    return [chapter_ids[round(i * step)] for i in range(n_samples)]

id = get_manga_id('Shitsurakue')
chapter = get_chapter_ids(id)
print(chapter)
