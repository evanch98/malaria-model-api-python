from flask import Flask, request

from preprocessing.preprocessing import predict_image, ImageURL

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Malaria Diagnosis API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


@app.get("/malaria")
def get_prediction():
    request_data = request.get_json()
    data = predict_image(ImageURL(url=request_data["url"]))
    return data, 200
