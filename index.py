import faiss
import numpy as np 
from embed import transform, model, device
from PIL import Image
import torch

"""
prototype.numpy()
prototype.numpy().reshape((1,1280)).astype(np.float32)
index.add(vector)

"""


# Take a dictionary embeddings where keys are manga titles and values are prototype tensors
def build_index(embeddings):

    # Create a Faiss index
    index = faiss.IndexFlatL2(1280)

    titles = []

    for manga, prototype_tensor in embeddings.items():
        
        prototype_tensor = prototype_tensor.to('cpu')
        vector = prototype_tensor.numpy().reshape((1,1280)).astype(np.float32)
        # Add each vector to the index
        index.add(vector)

        # Track titles in a list
        titles.append(manga)

    return index, titles

def query_index(image_path, titles, index):
    panels = Image.open(image_path)
    processed_image = transform(panels)
    processed_image = processed_image.to(device)
    
    with torch.no_grad():
        manga_tensor = model(torch.unsqueeze(processed_image, 0))
        manga_tensor = manga_tensor.to('cpu')
    
    vector = manga_tensor.numpy().reshape((1,1280)).astype(np.float32)

    distances, indices = index.search(vector, 3)
    return [titles[index_similar] for index_similar in indices[0]]



