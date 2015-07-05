from flask import Flask, render_template
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


import GIS

app = Flask(__name__)

utilities = {
    "toilet": {"data_name": "", "file": os.path.join(APP_ROOT, "Public_Toilets.csv")},
    "water": {"data_name": "", "file": os.path.join(APP_ROOT, "Drinking_Fountains.csv")},
    "food": {"data_name": "food", "file": ""},
    "shelter": {"data_name": "shelter", "file": ""},
}

@app.route('/')
def index():
    return render_template("index.html", utilities=utilities)

@app.route('/<utility>/<lat>,<long>')
def utility(utility, lat, long):
    nearest_utility = GIS.find_object((lat, long), utilities[utility]["data_name"], utilities[utility]["file"])
    direction = GIS.get_direction((lat, long), nearest_utility[0][1])
    current_location = GIS.get_human_readable_address(lat, long)
    return render_template("utility.html", utility=utility, current_location=current_location, direction=direction)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
