import torch
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
    self.ckpt_path = self.config.CHECKPOINT_PATH
    self.weights_path = self.config.WEIGHTS_PATH
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
    self.model = self._load_model()

  def _load_model(self):
    """Load the pre-trained ResNet model.

    Returns:
        _type_: pre-trained ResNet model.
    """
    self.model = FoodClassifier(num_classes=self.num_classes)
    state_dict = torch.load(self.weights_path)
    self.model.load_state_dict(state_dict)
    self.model.eval()
    return self.model

  def _load_labels(self) -> list[str]:
    """Load the labels for the classification model.

    Returns:
        list[str]: list of labels.
    """
    with open(self.label_path, 'r') as f:
      labels = [line.strip() for line in f.readlines()]
    return labels

  def _process_image_bytes(self, image_bytes: bytes) -> Image.Image:
    """Decode a base64 string to an image.
    1. Base64 string → bytes → PIL Image

    Args:
        base64_str (str): base64 string of the image.

    Returns:
        Image.Image: decoded image.
    """
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    return image

  def _preprocess_image_for_resnet(self, image_bytes: bytes) -> torch.Tensor:
    """Preprocess the base64 image for ResNet model.

    Args:
        base64_str (_type_): bytes of the image.

    Returns:
        torch.Tensor: preprocessed image tensor.
    """
    image = self._process_image_bytes(image_bytes)
    tensor = self.transform(image)
    tensor = tensor.unsqueeze(0)
    return tensor

  def _predict(self, input_tensor: torch.Tensor) -> str:
    """Make a prediction using the model.

    Args:
        input_tensor (torch.Tensor): input tensor for the model.

    Returns:
        str: predicted class label.
    """
    with torch.no_grad():
      output = self.model(input_tensor)  # shape: [1, num_classes]
      probs = torch.softmax(output, dim=1)
      pred_class = torch.argmax(probs, dim=1).item()
    return self.labels[pred_class]

  def inference(self, image_bytes: bytes) -> str:
    """Make an inference using the model.

    Args:
        image (bytes): bytes of the image.

    Returns:
        str: predicted class label.
    """
    # preprocess the image
    input_tensor = self._preprocess_image_for_resnet(image_bytes)
    # make prediction
    pred_class = self._predict(input_tensor)
    return pred_class
