from PIL import Image
from torchvision import transforms
import torch, timm , os, glob


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


transform = transforms.Compose([transforms.Lambda(lambda x: x.convert("RGB")), transforms.Resize(224), transforms.ToTensor(), transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])]) 
model = timm.create_model("caformer_s18.sail_in22k",pretrained=True, num_classes=0)
model = model.to(device)


for param in model.parameters():
    param.requires_grad = False


def embedding_manga(title):
    panels = glob.glob(f"dataset/{title}/*.jpg")
    
    images = [transform(Image.open(panel_file)) for panel_file in panels]

    manga_tensor = torch.stack(images).to(device)
    
    # Run through the models, transform from (50, 3, 224, 224) to (50, 1280)
    panel_vectors = model(manga_tensor)
    
    # Really need to dive back in what is shape and tensor dimensions ???

    # Average out the vector for each mangas (50 panels each), shape = (1280,)
    avg_panel_vector = torch.mean(panel_vectors, dim=0)

    return avg_panel_vector

if __name__ == "__main__":
    print(embedding_manga('Berserk'))