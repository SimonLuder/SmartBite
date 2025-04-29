from dataset import FoodDataset
from model import FoodClassifier

import pytorch_lightning as pl
from torch.utils.data import DataLoader
from torchvision import transforms
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger
import torch

# Dummy Beispiel (ersetzen durch echte Daten)
labels_path = f"/path/to/images"
image_path = f"/path/to/labels"

# Transforms
transform = transforms.Compose([
])

# Dataset & Dataloader
train_dataset = DATASET(image_paths, labels, transform=transform) # TODO put here dataset
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

val_dataset = FoodDataset(image_paths, labels, transform=transform) # TODO put here dataset
val_loader = DataLoader(val_dataset, batch_size=32)

# Modell
model = FoodClassifier(num_classes=101)

# W&B Logger
wandb_logger = WandbLogger(project="food-classification", log_model="all")

# Callbacks
checkpoint_cb = ModelCheckpoint(
    monitor="val_acc",
    mode="max",
    save_top_k=1,
    filename="best-model-{epoch:02d}-{val_acc:.2f}",
    save_weights_only=True,
)

earlystop_cb = EarlyStopping(
    monitor="val_acc",
    patience=5,
    mode="max",
    verbose=True,
)

# Trainer
trainer = pl.Trainer(
    max_epochs=20,
    accelerator="auto",
    devices="auto",
    logger=wandb_logger,
    callbacks=[checkpoint_cb, earlystop_cb],
)

# Training starten
trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader)
