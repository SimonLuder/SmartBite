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

To set up the repository and prepare the data pipeline, follow these steps:

1. **Clone the GitHub repository**
    ```sh
    git clone https://github.com/SimonLuder/SmartBite.git
    cd SmartBite
    ```

2. **Install the Python dependencies**
    Make sure your virtual environment is activated, then run:
    ```sh
    pip install -r requirements.txt
    ```

3. **Download and preprocess the dataset**
    - First, add a valid `.dvc/config.local` file (shared separately), which contains the access keys for the DigitalOcean Spaces object storage.
    - Then, pull the dataset with DVC:
      ```sh
      dvc pull
      ```
    - Finally, preprocess the data:
      ```sh
      python src/preprocess.py
      ```

---
