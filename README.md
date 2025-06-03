# SmartBite: Food Recognition & Nutrition Estimator

Project repository for the graded assignment from the MSE course "Machine Learning and Data in Operations​", Spring 2025​.

## Project Sturcture

```
smartbite/
│
├── .dvc/                         # DVC metadata and cache
├── .github/                      # GitHub Actions workflows

├── backend/
│   ├── src/
│   │   ├── controllers/          # API controllers (e.g. for orchestration)
│   │   ├── models/               # Pydantic models for request/response validation
│   │   ├── routes/               # API Endpoints
│   │   └── services/             # Core logic (ML model, data processing)
│   └── app.py                    # Entry point for the FastAPI backend
│   └── config.py                 # Configuration settings (e.g., API keys)
│
├── data/                         # Raw & processed datasets
│
├── dockerfile/
│   └── dockerfile.modeling.cuda  # Dockerfile for running the DVC pipeline
│
├── frontend/
│   ├── assets/                   # Static assets (images)
│   ├── pages/                    # Streamlit pages
│   ├── api.py                    # API client for communication with the backend
│   ├── frontend.dockerfile       # Dockerfile for the frontend
│   └── Home.py                   # Main Streamlit application file
│
├── src/
│   ├── dataset.py                # Defines the pytorch dataset
│   ├── evaluate.py               # Test script
│   ├── model.py                  # Defines the pytorch lightning model module
│   ├── preprocess.py             # Data preprocessing script
│   ├── train.py                  # Training script
│   └── utils.py                  # Utility functions
│
├── tests/                        # Integration tests for backend
│   ├── fixtures/                 # Sample data for testing
│   └── integration/              # Integration tests API endpoints
│
├── config.yaml                   # Configuration file for DVC
├── docker-compose.yml            # Docker Compose configuration for running the application
├── dvc.yaml                      # Configuration file for DVC pipeline (preprocess, trian, evaluate)
├── README.md
└── requirements.txt              # All Python dependencies
```

## Application Setup

To set up the repository and prepare the data pipeline, follow these steps:

### Cloning

**Clone the GitHub repository**

```sh
git clone https://github.com/SimonLuder/SmartBite.git
cd SmartBite
```

### Environment Variables

To run the application, you need to set up environment variables for the backend.

Please create a `.env` file in the `backend` directory with the following content:

- For the FatSecret API, you need to create an account [here](https://platform.fatsecret.com/platform-api).

```env
CLIENT_ID='<fatsecret_client_id>'
CLIENT_SECRET='<fatsecret_client_secret>'
NUTRITION_API_URL='https://platform.fatsecret.com/rest/foods/search/v1'
WEIGHTS_LOADING_APPROACH='wandb'
```

### Model Weights

To use the pre-trained model weights, you need to follow these steps:

1. Download the model weights from a new workflow which can be found [here](https://github.com/SimonLuder/SmartBite/actions).
2. Place the downloaded model weights in the `backend/src/static_files` directory.
3. Continue with the next steps to set up the application.

### Run the Application

The application can be started in two ways:

- Option 1: Use docker to run the backend and frontend
- Option 2: Run the backend and frontend separately

#### Option 1: Run with Docker

Make sure you have Docker installed and running.

- The application can be accessed at `http://localhost:8501/`

```sh
docker compose up --build
```

#### Option 2: Run Backend and Frontend Separately

_Install the Python dependencies_

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

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

1. Build the image

   ```sh
   docker build -f dockerfile/dockerfile.modeling.cuda -t pytorch-wandb-cuda .
   ```

2. Start the container as an interactive session

   ```sh
   docker run -it --rm --gpus all -v $(pwd):/app -w /app pytorch-wandb-cuda bash
   ```

3. Run the DVC pipeline. This automates the data download, pre-processing, model training and testing.

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

- The backend image can be found [here](https://github.com/users/SimonLuder/packages/container/package/smartbite-backend).
- The frontend image can be found [here](https://github.com/users/SimonLuder/packages/container/package/smartbite-frontend).

The application is accessible [here](https://smartbite-frontend.onrender.com).

---
