import torch
import torch.nn as nn
import torchvision.models as models
import pytorch_lightning as pl
import torchmetrics

class FoodClassifier(pl.LightningModule):
    def __init__(self, num_classes, lr=1e-4):
        super().__init__()
        self.save_hyperparameters()
        self.lr = lr

        self.model = models.resnet50(pretrained=True)
        # Freeze all layers except the last one
        # for param in self.model.parameters():
        #     param.requires_grad = False
        # for param in self.model.fc.parameters():
        #     param.requires_grad = True
        # # Unfreeze the last block
        # for param in self.model.layer4.parameters():
        #     param.requires_grad = True
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

        self.criterion = nn.CrossEntropyLoss()
        self.accuracy = torchmetrics.classification.Accuracy(task="multiclass", num_classes=num_classes)

        self.precision = torchmetrics.classification.MulticlassPrecision(num_classes=num_classes, average='macro')
        self.recall = torchmetrics.classification.MulticlassRecall(num_classes=num_classes, average='macro')

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        acc = self.accuracy(logits.softmax(dim=-1), y)
        precision = self.precision(logits.softmax(dim=-1), y)
        recall = self.recall(logits.softmax(dim=-1), y)
        self.log("train_precision", precision)
        self.log("train_recall", recall)
        self.log("train_loss", loss)
        self.log("train_acc", acc)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        acc = self.accuracy(logits.softmax(dim=-1), y)
        precision = self.precision(logits.softmax(dim=-1), y)
        recall = self.recall(logits.softmax(dim=-1), y)
        self.log("val_precision", precision, prog_bar=True)
        self.log("val_recall", recall, prog_bar=True)
        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", acc, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)
