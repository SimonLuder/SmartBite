from torchvision import transforms
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger
import wandb
from model import FoodClassifier
from dataset import ImageLabelDataset
from utils import load_config, save_config, wandb_run_exists
import json
import os
import shutil


def train_model(config=None):

    # Configuration
    if config is None:
        config = load_config()

    
    # W&B setup
    with open("wandb_secret.json", "r") as f:
        wandb_secret = json.load(f)

    if wandb_run_exists(config["entity"], config["project_name"], config["run_name"], wandb_secret["API_KEY"]):
        raise ValueError(f"A W&B run with the name {config['run_name']} already exists. Choose a different run_name in config.yaml")

    wandb.login(key=wandb_secret["API_KEY"])
    wandb_run = wandb.init(project=config["project_name"], entity=config["entity"], name=config["run_name"], config=config)
    wandb_logger = WandbLogger(experiment=wandb_run, log_model=config["wandb"]["log_model"])

    output_dir = f"models/{config['run_name']}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    # Transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225])
        ]
    )

    # Datasets
    train_dataset = ImageLabelDataset(
        json_path=config["dataset"]["train_json"],
        root_dir=config["dataset"]["images_dir"],
        transform=transform,
    )

    val_dataset = ImageLabelDataset(
        json_path=config["dataset"]["val_json"],
        root_dir=config["dataset"]["images_dir"],
        transform=transform,
    )

    # Dataloaders
    train_loader = DataLoader(train_dataset, batch_size=config["dataset"]["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=config["dataset"]["batch_size"])

    # Model
    model = FoodClassifier(
        num_classes=config["model"]["num_classes"],
        lr=config["model"]["lr"],
        out_dir=output_dir
    )

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
        max_epochs=config["trainer"]["max_epochs"],
        accelerator=config["trainer"]["accelerator"],
        devices=config["trainer"]["devices"],
        logger=wandb_logger,
        callbacks=[checkpoint_cb, earlystop_cb],
    )

    # Train
    trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader)

    # Update WandB logs
    run_id = wandb_run.id
    artifact_name = f"model-{run_id}"
    best_model_artifact_name = f"{config['entity']}/{config['project_name']}/{artifact_name}:best"
    config["wandb"]["run_id"] = run_id
    config["wandb"]["best_model_artifact_name"] = best_model_artifact_name
    wandb_run.config.update({"best_model_artifact_name": best_model_artifact_name}, allow_val_change=True)
    
    # Save the best model locally
    best_model_path = checkpoint_cb.best_model_path
    shutil.copy(best_model_path, os.path.join(output_dir, "best_model.pt"))
    save_config(os.path.join("temp", "config.yaml"), config)
    save_config(os.path.join(output_dir, "config.yaml"), config)

    # Finish run
    wandb.finish()

if __name__ == "__main__":
    train_model()