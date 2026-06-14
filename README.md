### Overview

This project is used for recommending manga based on their artstyle using pretrained CNN model

The data was scraped using Mangadex API


Project: Manga art style recommender. User uploads a panel → system returns visually similar manga titles based on art style.

### Tech stack: Python, PyTorch, Danbooru-pretrained ViT/ResNet, Faiss, FastAPI.


### Concepts fully covered:

- [x] CNNs, early/mid/late layers, why style lives in early/mid layers
- [x] Why Danbooru-pretrained > ImageNet for this task
- [ ] Preprocessing pipeline: resize 224x224 → replicate grayscale to 3 channels → normalize → (3,224,224) tensor
- [ ] Feature extraction: frozen weights, 1280-dim embedding from second-to-last layer
- [ ] Mean pooling 50 panels → one prototype vector per manga title
- [ ] Faiss for nearest-neighbor search at scale
- [ ] Contrastive loss fine-tuning (concept only, not implemented)

### Setup


### Usage
Add the panels of your favourite manga in and it will return mangas with similar artstyle for you. 

