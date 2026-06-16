from fastapi import FastAPI, UploadFile
from embed import embedding_manga
from index import build_index, query_index
import os 

app = FastAPI()

# Startup — build index once
panels = os.listdir("dataset/")
embeddings = {title: embedding_manga(title) for title in panels}
index, titles = build_index(embeddings)

@app.post("/recommend")
async def recommend(image: UploadFile):
    # 1. Save uploaded file to disk
    with open("temp_panel.jpg", "wb") as f:
        f.write(await image.read())
    
    # 2. Query the index
    results = query_index("temp_panel.jpg", index, titles)
    
    # 3. Return results
    return {"recommendations": results}