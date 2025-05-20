# SmartBite: Food Recognition & Nutrition Estimator

Project repository for the graded assignment from the MSE course "Machine Learning and Data in Operations​", Spring 2025​.

## Project Sturcture

```
smartbite/
│
├── backend/
|   ├── src/
│   │   ├── controllers/      # API controllers (e.g. for orchestration)
|   │   ├── models/           # Pydantic models for request/response validation
|   │   ├── routes/           # API Endpoints
|   │   ├── services/         # Core logic (ML model, data processing)
│   └── app.py                # Entry point for the FastAPI backend
|   └── config.py             # Configuration settings (e.g., API keys)
│
├── dashboard/
│   └── app.py                 # Streamlit frontend
│
├── data/                      # Raw & processed datasets
│
├── notebooks/                 # Jupyter Notebooks for EDA, prototyping
│
├── src/                       # Core logic
│   ├── train.py
│   └── evaluate.py
│
├── dvc.yaml                   # DVC pipeline config
├── Dockerfile                 # Container for API/Streamlit
├── README.md
├── requirements.txt           # All Python dependencies
├── .dvc/
└── .gitignore
```

## Repository Setup

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

### Backend Setup

**Run the FastAPI backend**

The backend runs on port 8000 by default.

```sh
cd backend
uvicorn app:app --reload
```

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

---
