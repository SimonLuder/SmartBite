import time
import random


### fake API function to simulate image analysis ###
def analyze_image(image_file):
    time.sleep(5)  # Simulate loading time

    fake_labels = ["Pizza", "Sushi", "Burger", "Salad", "Pasta", "Wrap"]
    label = random.choice(fake_labels)

    return {
        "label": label,
        "confidence": round(random.uniform(0.7, 0.99), 2),
        "nutrition": {
            "calories": random.randint(250, 600),
            "protein": round(random.uniform(5, 30), 1),
            "carbohydrates": round(random.uniform(20, 70), 1),
            "fat": round(random.uniform(5, 30), 1),
        }
    }