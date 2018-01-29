import os
import time
import airquality
from flask import Flask, url_for, render_template
import configparser
from flask_googlemaps import GoogleMaps


app = Flask(__name__)
ISPROD = os.environ.get('IS_HEROKU', None)

# Load API key from .env if exists
if ( os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))

    # Initialize the extension
    GoogleMaps(app, key=config['API']['GOOGLE_MAPS'])
else:
    GoogleMaps(app, key=os.environ.get('GOOGLE_MAPS', None))


def get_data():
    try:
        air_data = get_data.air_data
        over40 = get_data.over40
        over200 = get_data.over200
    except AttributeError:
        air_data = {'Wells Rd': {'time': 0},
                    'Bristol Depot': {'time': 0},
                    'Parson St': {'time': 0},
                    'Fishponds': {'time': 0}}
        over40 = {}
        over200 = {}

    for key in airquality.AREAS:
        if (time.time() - air_data[key]['time']) > (15 * 60):
            air_data[key] = airquality.get_air_dict(key, False)
            if air_data[key]['NO215m'] > airquality.NO2YLM:
                over40[key] = air_data[key]['NO215m']
            if air_data[key]['NO224h'] > airquality.NO215LM:
                over200[key] = air_data[key]['NO224h']

    get_data.air_data = air_data
    get_data.over40 = over40
    get_data.over200 = over200

    return air_data, over40, over200


@app.route("/")
def choking():
    [air_data, over40, over200] = get_data()

    return render_template('index.html', airdata=air_data, url=[airquality.URL, airquality.SITEURL], urlcodes=airquality.AREAS,  areas=over40.keys(), choking=len(over40), time=time.time(), over200=over200 )


with app.test_request_context():
    url_for('static', filename='style.css')
