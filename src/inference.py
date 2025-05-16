import base64
from io import BytesIO
from PIL import Image
import torch
from torchvision import transforms
import torch

from model import FoodClassifier


# 1. Base64 string → bytes → PIL Image
def decode_base64_image(base64_str):
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data)).convert("RGB")
    return image

# 2. Define transforms for ResNet (e.g., ResNet-50)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def preprocess_base64_for_resnet(base64_str):
    image = decode_base64_image(base64_str)
    tensor = transform(image)
    tensor = tensor.unsqueeze(0)
    return tensor

def load_model(weights_path, num_classes=101):
    model = FoodClassifier(num_classes=num_classes)
    state_dict = torch.load(weights_path)
    model.load_state_dict(state_dict)
    model.eval()
    return model

labels= [
    "Apple pie",
    "Baby back ribs",
    "Baklava",
    "Beef carpaccio",
    "Beef tartare",
    "Beet salad",
    "Beignets",
    "Bibimbap",
    "Bread pudding",
    "Breakfast burrito",
    "Bruschetta",
    "Caesar salad",
    "Cannoli",
    "Caprese salad",
    "Carrot cake",
    "Ceviche",
    "Cheesecake",
    "Cheese plate",
    "Chicken curry",
    "Chicken quesadilla",
    "Chicken wings",
    "Chocolate cake",
    "Chocolate mousse",
    "Churros",
    "Clam chowder",
    "Club sandwich",
    "Crab cakes",
    "Creme brulee",
    "Croque madame",
    "Cup cakes",
    "Deviled eggs",
    "Donuts",
    "Dumplings",
    "Edamame",
    "Eggs benedict",
    "Escargots",
    "Falafel",
    "Filet mignon",
    "Fish and chips",
    "Foie gras",
    "French fries",
    "French onion soup",
    "French toast",
    "Fried calamari",
    "Fried rice",
    "Frozen yogurt",
    "Garlic bread",
    "Gnocchi",
    "Greek salad",
    "Grilled cheese sandwich",
    "Grilled salmon",
    "Guacamole",
    "Gyoza",
    "Hamburger",
    "Hot and sour soup",
    "Hot dog",
    "Huevos rancheros",
    "Hummus",
    "Ice cream",
    "Lasagna",
    "Lobster bisque",
    "Lobster roll sandwich",
    "Macaroni and cheese",
    "Macarons",
    "Miso soup",
    "Mussels",
    "Nachos",
    "Omelette",
    "Onion rings",
    "Oysters",
    "Pad thai",
    "Paella",
    "Pancakes",
    "Panna cotta",
    "Peking duck",
    "Pho",
    "Pizza",
    "Pork chop",
    "Poutine",
    "Prime rib",
    "Pulled pork sandwich",
    "Ramen",
    "Ravioli",
    "Red velvet cake",
    "Risotto",
    "Samosa",
    "Sashimi",
    "Scallops",
    "Seaweed salad",
    "Shrimp and grits",
    "Spaghetti bolognese",
    "Spaghetti carbonara",
    "Spring rolls",
    "Steak",
    "Strawberry shortcake",
    "Sushi",
    "Tacos",
    "Takoyaki",
    "Tiramisu",
    "Tuna tartare",
    "Waffles"
  ]

def predict(model, input_tensor):
    with torch.no_grad():
        output = model(input_tensor)  # shape: [1, num_classes]
        probs = torch.softmax(output, dim=1)
        pred_class = torch.argmax(probs, dim=1).item()
    return labels[pred_class]


def inference(base64_str, model):
    # Preprocess the image
    input_tensor = preprocess_base64_for_resnet(base64_str)
    # Make prediction
    pred_class = predict(model, input_tensor)
    return pred_class