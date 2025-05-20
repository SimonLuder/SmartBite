import os
import json
from PIL import Image
from torch.utils.data import Dataset

class ImageLabelDataset(Dataset):
    def __init__(self, json_path, root_dir, transform=None):
        with open(json_path, 'r') as f:
            data = json.load(f)

        self.samples = data["samples"]
        self.classes = data["classes"]  # folder-style class names (e.g., apple_pie)
        self.labels = data["labels"]    # human-readable names (e.g., Apple Pie)

        # Index classes by their position
        self.class_to_idx = {class_name: idx for idx, class_name in enumerate(self.classes)}
        
        self.image_label_pairs = []
        self.transform = transform
        self.root_dir = root_dir

        for class_name, image_list in self.samples.items():
            if class_name not in self.class_to_idx:
                raise ValueError(f"Class {class_name} not found in classes list.")
            label_idx = self.class_to_idx[class_name]
            for image_path in image_list:
                self.image_label_pairs.append((image_path, label_idx))


    def __len__(self):
        return len(self.image_label_pairs)


    def __getitem__(self, idx):
        img_path, label = self.image_label_pairs[idx]
        full_path = os.path.join(self.root_dir, img_path)
        image = Image.open(full_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, label