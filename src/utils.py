import yaml
import os
import wandb
import shutil


def load_config(path="config.yaml"):
    """To load the yaml yonfig file"""
    with open(path, "r") as f:
        return yaml.safe_load(f)
    

def save_config(path, config):
    with open(path, "w") as f:
            yaml.safe_dump(config, f)


def get_run_id_from_name(entity: str, project: str, run_name: str) -> str:
    """
    Uses the W&B API to fetch the run ID from a run name.

    Args:
        entity (str): Your W&B username or team
        project (str): W&B project name
        run_name (str): The human-readable run name

    Returns:
        str: The W&B run ID
    """
    api = wandb.Api()
    runs = api.runs(f"{entity}/{project}")

    for run in runs:
        if run.name == run_name:
            return run.id

    raise ValueError(f"No run found with name '{run_name}' in project '{project}'")


def download_best_model_artifact(entity: str, project: str, run_id: str, output_dir: str = "temp"):
    """
    Downloads the best model artifact from a W&B run into a unique subfolder.

    Args:
        entity (str): W&B entity
        project (str): W&B project name
        run_id (str): W&B run ID (not run name!)
        output_dir (str): Base directory to store artifacts

    Returns:
        str: Path to the downloaded checkpoint file
    """
    artifact_name = f"model-{run_id}:latest"
    full_artifact_path = f"{entity}/{project}/{artifact_name}"

    # Create a subfolder for this run
    run_subfolder = os.path.join(output_dir, run_id)
    os.makedirs(run_subfolder, exist_ok=True)

    print(f"Downloading artifact: {full_artifact_path} into {run_subfolder}")
    artifact = wandb.use_artifact(full_artifact_path, type="model")

    # Download to a temp folder first (W&B doesn't support direct download into custom folder)
    temp_dir = artifact.download()

    for filename in os.listdir(temp_dir):
        src_path = os.path.join(temp_dir, filename)
        dst_path = os.path.join(run_subfolder, filename)

        # If destination file exists, delete it
        if os.path.exists(dst_path):
            os.remove(dst_path)

        shutil.move(src_path, dst_path)

    # Cleanup temp folder
    shutil.rmtree(temp_dir)

    # Get checkpoint file
    ckpt_files = [f for f in os.listdir(run_subfolder) if f.endswith(".ckpt")]
    if not ckpt_files:
        raise FileNotFoundError("No .ckpt file found in downloaded artifact.")

    ckpt_path = os.path.join(run_subfolder, ckpt_files[0])
    print(f"Checkpoint downloaded to: {ckpt_path}")
    return ckpt_path

def wandb_run_exists(entity, project, run_name, api_key):
    api = wandb.Api(api_key=api_key)
    runs = api.runs(f"{entity}/{project}")
    return any(run.name == run_name for run in runs)