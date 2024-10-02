from flask import Flask, request

from preprocessing.preprocessing import predict_image, ImageURL

app = Flask(__name__)

@app.get("/malaria")
def get_prediction():
    request_data = request.get_json()
    data = predict_image(ImageURL(url=request_data["url"]))
    return data, 200
