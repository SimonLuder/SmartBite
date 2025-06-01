import os
import torch
import torch.nn as nn
import torchvision.models as models
import pytorch_lightning as pl
from torchmetrics.classification import Accuracy, Precision, Recall, MulticlassAccuracy


class FoodClassifier(pl.LightningModule):
    def __init__(self, num_classes, lr=1e-4, out_dir=None):
        super().__init__()
        self.save_hyperparameters()

        self.model = models.resnet50(pretrained=True) # Backbone
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes) # Classifier layer

        self.lr = lr
        self.criterion = nn.CrossEntropyLoss()
        
        # Used separate instances for train/val to avoid state leakage
        self.train_acc = Accuracy(task="multiclass", num_classes=num_classes)
        self.train_precision = Precision(task="multiclass", num_classes=num_classes, average='macro')
        self.train_recall = Recall(task="multiclass", num_classes=num_classes, average='macro')

        self.val_acc = Accuracy(task="multiclass", num_classes=num_classes)
        self.val_precision = Precision(task="multiclass", num_classes=num_classes, average='macro')
        self.val_recall = Recall(task="multiclass", num_classes=num_classes, average='macro')

        self.out_dir = out_dir


    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        acc = self.train_acc(logits.softmax(dim=-1), y)
        precision = self.train_precision(logits.softmax(dim=-1), y)
        recall = self.train_recall(logits.softmax(dim=-1), y)
        self.log("train_precision", precision)
        self.log("train_recall", recall)
        self.log("train_loss", loss)
        self.log("train_acc", acc)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        acc = self.val_acc(logits.softmax(dim=-1), y)
        precision = self.val_precision(logits.softmax(dim=-1), y)
        recall = self.val_recall(logits.softmax(dim=-1), y)
        self.log("val_precision", precision, prog_bar=True)
        self.log("val_recall", recall, prog_bar=True)
        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", acc, prog_bar=True)
        

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)
    

    def on_test_start(self):
        self.test_preds = []
        self.test_targets = []

        # Per-class accuracy
        self.per_class_accuracy = MulticlassAccuracy(
            num_classes=self.hparams.num_classes, average=None).to(self.device)


    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)

        probs = torch.nn.functional.softmax(logits, dim=1)
        preds = probs.argmax(dim=1)

        # Save for confusion matrix
        self.test_preds.append(preds.cpu())
        self.test_targets.append(y.cpu())

        # Log metrics
        acc = self.val_acc(probs, y)
        precision = self.val_precision(probs, y)
        recall = self.val_recall(probs, y)

        self.log("test_loss", loss)
        self.log("test_acc", acc)
        self.log("test_precision", precision)
        self.log("test_recall", recall)
        

    def on_test_end(self):
        # Stack and save predictions and targets for confusion matrix
        preds = torch.cat(self.test_preds)
        targets = torch.cat(self.test_targets)
        if self.out_dir:
            torch.save({"preds": preds, "targets": targets}, os.path.join(self.out_dir, "test_outputs.pt"))
    
