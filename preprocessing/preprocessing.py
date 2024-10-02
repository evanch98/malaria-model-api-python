import numpy as np
import cv2
import requests
from pydantic import BaseModel

from malaria_model.malaria_model import model


class ImageURL(BaseModel):
    url: str


IM_SIZE = 224


# Preprocess the image
def preprocess_image(image_url, target_size=(IM_SIZE, IM_SIZE)):
    # load the image from URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.google.com/',  # Set the referer to the source domain or Google
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(image_url, headers=headers)

    if response.status_code == 200:
        # convert the image data to a NumPy array
        image = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Decode the image

        # resize the image to the target size (same as training)
        image = cv2.resize(image, target_size)

        # convert image to array and normalize
        image = image / 255.0

        # add batch dimension
        image = np.expand_dims(image, axis=0)

        return image
    else:
        raise ValueError(f"Failed to download image. HTTP status code: {response.status_code}")


# Tag the image
def parasite_or_not(x):
    if x < 0.5:
        return str('Parasitized')
    else:
        return str('Uninfected')


# Predict the image
def predict_image(image_url: ImageURL):
    # preprocess the image
    image = preprocess_image(image_url.url)

    # make prediction
    prediction = model.predict(image)

    # get the predicted class
    predicted_class = parasite_or_not(prediction[0][0])

    return {"predicted_class": predicted_class, "confidence": float(np.max(prediction))}
