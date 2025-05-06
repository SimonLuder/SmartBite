
from model import FoodClassifier

import pytorch_lightning as pl
from torch.utils.data import DataLoader
from torchvision import transforms
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

# append src to path
from dataset import ImageLabelDataset

# Transforms (hier deine gewünschten Operationen einfügen)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


# Datasets
train_dataset = ImageLabelDataset(
    json_path=r'data/processed/food-101/train.json',
    root_dir=r'data/raw/food-101/images',
    transform=transform,
    )
val_dataset = ImageLabelDataset(
    json_path=r'data/processed/food-101/test.json',
    root_dir=r'data/raw/food-101/images',
    transform=transform,
    )

# Dataloaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)

# Modell
model = FoodClassifier(num_classes=101, lr=1e-4)

# W&B Logger
wandb_logger = WandbLogger(project="smartbite", log_model="all")

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
