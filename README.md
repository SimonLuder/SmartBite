# SmartBite: Food Recognition & Nutrition Estimator

Project repository for the graded assignment from the MSE course "Machine Learning and Data in Operations​", Spring 2025​.

## Project Sturcture
```
smartbite/
│
├── api/
│   └── main.py                # FastAPI backend
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

To set up the repository, follow the subsequent steps:

1. Clone the GitHub repository
    ```sh
    git clone https://github.com/SimonLuder/SmartBite.git
    ```

2. Install the dependencies from the requirements.txt
    ```sh
    pip install -r requirements.txt
    ```

3. Download the dataset
First, add `.dvc/config.local` (obtained separately) which contains the access keys for the DigitalOcean space object storage. Next, pull the current dataset.
    ```sh
    dvc pull
    ```