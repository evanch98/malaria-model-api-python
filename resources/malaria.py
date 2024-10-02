from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from preprocessing.preprocessing import predict_image, ImageURL

blp = Blueprint("malaria", __name__, description="Operations on malaria")

@blp.route("/malaria")
class Malaria(MethodView):
    @blp.response(200)
    def get(self):
        request_data = request.get_json()
        try:
            data = predict_image(ImageURL(url=request_data["url"]))
            return data, 200
        except KeyError:
            abort(404, message="Not Found.")
