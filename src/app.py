from flask import Flask, render_template
from shapely import Point
import SEPTAFinder

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

# call SEPTAFinder using coordinate parameters
# param format: xxxx,yyyy
# GET
@app.route("/get-nearest-station/<coords>", methods=["GET"])
def get_nearest_station(coords):
    _coords_ = str.split(coords, ',')
    return SEPTAFinder.SEPTAFinder(Point(float(_coords_[0]), float(_coords_[1])))

if __name__ == "__main__":
    app.run(debug=True)