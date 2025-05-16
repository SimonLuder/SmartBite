import os
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger

import wandb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

from dataset import ImageLabelDataset
from model import FoodClassifier  # Your LightningModule
from utils import load_config, download_best_model_artifact, get_run_id_from_name


def test_model(config=None):

    if config is None:
        config = load_config()

    entity = config["entity"]
    project = config["project_name"]
    name = config["run_name"]

    run_id = get_run_id_from_name(entity, project, config["run_name"])
    wandb_run = wandb.init(project=project, entity=entity, id=run_id, resume="allow", name=name, config=config)
    wandb_logger = WandbLogger(experiment=wandb_run)
    ckpt_path = download_best_model_artifact(entity, project, run_id, "temp/")

    # Load model
    model = FoodClassifier.load_from_checkpoint(ckpt_path, num_classes=config["model"]["num_classes"])
    model.eval()

    # Transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    test_dataset = ImageLabelDataset(
        config["dataset"]["test_json"],
        config["dataset"]["images_dir"],
        transform
    )
    test_loader = DataLoader(test_dataset, batch_size=config["dataset"]["batch_size"])

    # Trainer
    trainer = pl.Trainer(
        logger=wandb_logger,
        accelerator=config["trainer"]["accelerator"],
        devices=config["trainer"]["devices"]
    )
    # Run Test
    trainer.test(model, dataloaders=test_loader)

    # Load predictions
    outputs = torch.load("temp/test_outputs.pt")
    preds = outputs["preds"].numpy()
    targets = outputs["targets"].numpy()

    # Confusion Matrix
    cm = confusion_matrix(targets, preds)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=False, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.savefig("temp/confusion_matrix.png")
    plt.close()

    # accuracy per class = correctly predicted / total in that class (row-wise)
    true_positives = np.diag(cm)
    samples_per_class = cm.sum(axis=1)
    per_class_acc = np.divide(
        true_positives, 
        samples_per_class, 
        out=np.zeros_like(true_positives, dtype=np.float32), 
        where=samples_per_class != 0
    )

    # Plot
    plt.figure(figsize=(18, 5))
    plt.bar(range(len(per_class_acc)), per_class_acc)
    plt.xlabel("Class ID")
    plt.ylabel("Accuracy")
    plt.title("Per-Class Accuracy")
    plt.tight_layout()
    plt.savefig("temp/per_class_accuracy.png")
    plt.close()

    # Log confusion matrix image to W&B
    wandb.log({"confusion_matrix": wandb.Image("temp/confusion_matrix.png")})

    # Upload test predictions as W&B artifact
    wandb.log({"per_class_accuracy": wandb.Image("temp/per_class_accuracy.png")})

    # Finish run
    wandb.finish()


if __name__ == "__main__":

    test_model()
