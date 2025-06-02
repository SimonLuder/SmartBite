FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# preload resnet50 model weights
# we need to to this to avoid downloading the model weights at runtime
# which would slow down the application startup
RUN python -c "import torchvision.models as models; models.resnet50(weights=models.ResNet50_Weights.DEFAULT)"

COPY backend/ .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
