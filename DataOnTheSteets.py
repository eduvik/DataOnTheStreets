from flask import Flask, render_template

import GIS

app = Flask(__name__)

utilities = ["toilet", "water", "food", "shelter"]

@app.route('/')
def index():
    return render_template("index.html", utilities=utilities)

@app.route('/<utility>/<lat>,<long>')
def utility(utility, lat, long):
    nearest_utility = GIS.find_object((lat, long), utility)
    direction = GIS.get_direction((lat, long), nearest_utility[0][1])
    current_location = GIS.get_human_readable_address(lat, long)
    return render_template("utility.html", utility=utility, current_location=current_location, direction=direction)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
