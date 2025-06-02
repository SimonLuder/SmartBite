import torch
import json
from torchvision import transforms
from io import BytesIO
from PIL import Image

import config
from .model import FoodClassifier


class ClassificationModel:
  _instance = None

  @staticmethod
  def get_instance():
    """Singleton pattern to get the instance of the classification model."""
    if ClassificationModel._instance is None:
      ClassificationModel._instance = ClassificationModel()
    return ClassificationModel._instance

  def __init__(self):
    """Initialize the classification model."""
    self.config = config.get_config()
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    self.label_path = self.config.LABEL_PATH
    self.num_classes = 101
    self.labels = self._load_labels()
    self.transform = transforms.Compose(
      [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
      ]
    )

    # here we can choose to load the model from wandb or from local weights
    if self.config.WEIGHTS_LOADING_APPROACH == 'wandb':
      self.ckpt_path = self.config.CHECKPOINT_PATH
      self.model = self._load_model_wandb()
    else:
      self.weights_path = self.config.WEIGHTS_PATH
      self.model = self._load_model_default()

  def _load_model_default(self) -> FoodClassifier:
    """Load the finetuned ResNet model from a .pth file.

    Returns:
        FoodClassifier: pre-trained ResNet model.
    """
    self.model = FoodClassifier(num_classes=self.num_classes)
    state_dict = torch.load(self.weights_path)
    self.model.load_state_dict(state_dict)
    self.model.eval()
    self.model.to(self.device)
    return self.model

  def _load_model_wandb(self) -> FoodClassifier:
    """Load the finetuned ResNet model from a .ckpt file.
    This file is loaded from wandb.

    Returns:
        FoodClassifier: pre-trained ResNet model.
    """
    self.model = FoodClassifier(num_classes=self.num_classes)
    state_dict = torch.load(self.ckpt_path, map_location=self.device)
    self.model.load_state_dict(state_dict.get('state_dict'))
    self.model.eval()
    self.model.to(self.device)
    return self.model

  def _load_labels(self) -> list[str]:
    """Load the labels for the classification model.

    Returns:
        list[str]: list of labels.
    """
    with open(self.label_path, 'r') as f:
      # load the labels from the json file
      labels = json.load(f)
    return labels

  def _process_image_bytes(self, image_bytes: bytes) -> Image.Image:
    """Decode a bytes image to a PIL Image.

    Args:
        image_bytes (bytes): bytes of the image.

    Returns:
        Image.Image: decoded image.
    """
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return image

  def _preprocess_image_for_resnet(self, image_bytes: bytes) -> torch.Tensor:
    """Preprocess the bytes image for ResNet model.

    Args:
        image_bytes (bytes): bytes of the image.

    Returns:
        torch.Tensor: preprocessed image tensor.
    """
    image = self._process_image_bytes(image_bytes)
    tensor = self.transform(image)
    tensor = tensor.unsqueeze(0)
    return tensor

  def _predict(self, input_tensor: torch.Tensor) -> tuple[str, float]:
    """Make a prediction using the model.

    Args:
        input_tensor (torch.Tensor): input tensor for the model.

    Returns:
        tuple[str, float]: predicted class label and probability.
    """
    with torch.no_grad():
      output = self.model(input_tensor)  # shape: [1, num_classes]
      probs = torch.softmax(output, dim=1)
      # get the predicted class index
      pred_class = torch.argmax(probs, dim=1).item()
      # get prob for predicted class
      pred_prob = probs[0][pred_class].item()

    return self.labels[pred_class], pred_prob

  def inference(self, image_bytes: bytes) -> tuple[str, float]:
    """Make an inference using the model.

    Args:
        image_bytes (bytes): bytes of the image.

    Returns:
        tuple[str, float]: predicted class label and probability.
    """
    # preprocess the image
    input_tensor = self._preprocess_image_for_resnet(image_bytes).to(self.device)

    # make prediction
    pred_class, probability = self._predict(input_tensor)

    return pred_class, probability
