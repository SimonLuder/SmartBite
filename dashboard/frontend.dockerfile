FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard/ .

CMD ["streamlit", "run", "Home.py", "--server.port=8501"]
