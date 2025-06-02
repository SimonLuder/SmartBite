import torch.nn as nn
import torchvision.models as models


class FoodClassifier(nn.Module):
  def __init__(self, num_classes=101):
    super().__init__()
    self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)  # Backbone
    self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)  # Classifier layer

  def forward(self, x):
    return self.model(x)
