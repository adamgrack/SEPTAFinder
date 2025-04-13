from flask import Flask, request, jsonify
from shapely import Point
import SEPTAFinder

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Home"

@app.route("/get-nearest-station/<coords>", methods=["GET"])
def get_nearest_station(coords):
    _coords_ = Point(coords[0], coords[1])
    return SEPTAFinder.SEPTAFinder(_coords_)

if __name__ == "__main__":
    app.run(debug=True)