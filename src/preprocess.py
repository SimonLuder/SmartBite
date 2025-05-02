import os
import json
import random
from pathlib import Path
import shutil
from typing import Tuple, Dict, List
from sklearn.model_selection import train_test_split

RAW_DIR = Path("data/raw/food-101/images")
META_DIR = Path("data/raw/food-101/meta")
OUT_DIR = Path("data/processed/food-101")

VAL_SPLIT = 0.5
SEED = 42

def load_json(json_path: Path) -> Dict:
    with open(json_path, "r") as f:
        return json.load(f)

def load_txt(txt_path: Path) -> List[str]:
    with open(txt_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def split_val_test(data: Dict, test_ratio: int = 0.5, random_state: int = 42) -> Tuple[Dict, Dict]:
    val_split = {}
    test_split = {}
    for class_name, samples in data.items():
        val_samples, test_samples = train_test_split(
            samples, test_size=test_ratio, random_state=random_state
        )
        val_split[class_name] = val_samples
        test_split[class_name] = test_samples
    return val_split, test_split

def build_file_index(root_dir: str, extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp")) -> Dict[str, str]:
    file_index = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith(extensions):
                rel_dir = os.path.relpath(dirpath, root_dir)
                base_name, _ = os.path.splitext(fname)
                key = os.path.join(rel_dir, base_name).replace("\\", "/")
                value = os.path.join(rel_dir, fname).replace("\\", "/")
                file_index[key] = value
    return file_index

def complete_sample_paths(dataset_dict: Dict[str, List[str]], root_dir: str) -> Dict[str, List[str]]:
    file_index = build_file_index(root_dir)
    completed_dict = {}
    for class_name, samples in dataset_dict.items():
        updated_samples = []
        for sample in samples:
            if sample in file_index:
                updated_samples.append(file_index[sample])
            else:
                print(f"[WARN] Missing file for: {sample}")
        completed_dict[class_name] = updated_samples
    return completed_dict

def save_dataset_with_metadata(dataset: Dict, out_path: Path, classes: List[str], labels: List[str]):
    data_to_save = {
        "samples": dataset,
        "classes": classes,
        "labels": labels
    }
    with open(out_path, "w") as f:
        json.dump(data_to_save, f, indent=2)

def main():
    random.seed(SEED)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load metadata
    train_samples = load_json(META_DIR / "train.json")
    test_samples_full = load_json(META_DIR / "test.json")
    classes = load_txt(META_DIR / "classes.txt")
    labels = load_txt(META_DIR / "labels.txt")

    # Split test into val and test
    val_samples, test_samples = split_val_test(test_samples_full, VAL_SPLIT, SEED)

    # Complete sample paths
    train_samples = complete_sample_paths(train_samples, RAW_DIR)
    val_samples   = complete_sample_paths(val_samples, RAW_DIR)
    test_samples  = complete_sample_paths(test_samples, RAW_DIR)

    # Save datasets with classes and labels embedded
    save_dataset_with_metadata(train_samples, OUT_DIR / "train.json", classes, labels)
    save_dataset_with_metadata(val_samples, OUT_DIR / "val.json", classes, labels)
    save_dataset_with_metadata(test_samples, OUT_DIR / "test.json", classes, labels)

    print("Preprocessing complete.")

if __name__ == "__main__":
    main()
