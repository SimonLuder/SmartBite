# SmartBite: Food Recognition & Nutrition Estimator

Project repository for the graded assignment from the MSE course "Machine Learning and Data in Operations​", Spring 2025​.

## Project Sturcture

```
smartbite/
│
├── .dvc/
│
├── backend/
|   ├── src/
│   │   ├── controllers/      # API controllers (e.g. for orchestration)
|   │   ├── models/           # Pydantic models for request/response validation
|   │   ├── routes/           # API Endpoints
|   │   └── services/         # Core logic (ML model, data processing)
│   └── app.py                # Entry point for the FastAPI backend
|   └── config.py             # Configuration settings (e.g., API keys)
│
├── frontend/
│   └── app.py                 # Streamlit frontend
│
├── data/                      # Raw & processed datasets
│
├── notebooks/                 # Jupyter Notebooks for EDA, prototyping
│
├── src/                       # Core logic
│   ├── preprocess.py
│   ├── dataset.py             # Defines the pytorch dataset
│   ├── model.py               # Defines the pytorch lightning model module
│   ├── train.py               # Training script 
│   ├── evaluate.py            # Test script
│   └── inference.py           # Sample functions for inference
│
├── tests/                     # Integration tests for backend
│   ├── fixtures/              # Sample data for testing
│   └── integration/           # Integration tests API endpoints
│
├── dvc.yaml                   # DVC pipeline config
├── docker-compose.yml         # Docker Compose configuration for running the application
├── README.md
└── requirements.txt           # All Python dependencies
├── .dvc/
└── .gitignore
```

## Application Setup

To set up the repository and prepare the data pipeline, follow these steps:

### Cloning and Dependency Installation

**Clone the GitHub repository**

```sh
git clone https://github.com/SimonLuder/SmartBite.git
cd SmartBite
```

**Install the Python dependencies**

Make sure your virtual environment is activated, then run:

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Application

The application can be started in two ways:

- use docker to run the backend and frontend
- run the backend and frontend separately

#### Option 1: Run with Docker

Make sure you have Docker installed and running.

```sh
docker compose up --build
```

#### Option 2: Run Backend and Frontend Separately

_Run the FastAPI backend_

- The backend runs on port 8000 by default.

```sh
cd backend
uvicorn app:app --reload
```

_Run the Streamlit frontend_

- The frontend runs on port 8501 by default.

```sh
cd frontend
streamlit run Home.py
```

## ML-Pipline Overview

The machine learning pipeline consists of the following steps:

### Data Version Control (DVC) Setup

**Download and preprocess the dataset**

1. First, add a valid `.dvc/config.local` file (shared separately), which contains the access keys for the DigitalOcean Spaces object storage.

2. Then, pull the dataset with DVC:

   ```sh
   dvc pull
   ```

3. Finally, preprocess the data:

   ```sh
   python src/preprocess.py
   ```

### Run the training pipeline 

Optional: Build the docker image and run the code within the container

   Build the image
   ```sh
   docker build -f dockerfile/dockerfile.modeling.cuda -t pytorch-wandb-cuda .
   ```

   Start the container as an interactive session
   ```sh
   docker run -it --rm --gpus all -v $(pwd):/app -w /app pytorch-wandb-cuda bash
   ```

   Run the DVC pipeline. This automates the data download, pre-processing, model training and testing.
   ```sh
   dvc repro
   ```

### GitHub Actions

The repository is set up with GitHub Actions which automatically run on every push to the `main` branch. The actions include:

- **Tests**: Run integration tests to ensure the API endpoints are functioning correctly.
- **Download Model Weights**: Download the latest model weights from Weights & Biases to ensure that the backend uses the most up-to-date model.
- **Docker Images**: Build and push Docker images for the backend and frontend to the GitHub Container Registry.

### Deployment

The application is deployed on Render.com, which pulls the latest Docker images from the GitHub Container Registry and runs them.

The application is accessible [here](https://smartbite-frontend.onrender.com).

---
