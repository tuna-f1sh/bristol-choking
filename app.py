import os
import time
import airquality
from flask import Flask, url_for, render_template
import configparser
from flask_googlemaps import GoogleMaps
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)


# Load API key from .env if exists
if ( os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env'))

    # Initialize the extension
    GoogleMaps(app, key=config['API']['GOOGLE_MAPS'])
else:
    print("environ")
    GoogleMaps(app, key=os.environ.get('GOOGLE_MAPS', None))


def get_data():
    try:
        air_data = get_data.air_data
        over40 = get_data.over40
        over200 = get_data.over200
    except AttributeError:
        air_data = {'Wells Rd': {'time': 0, 'error': 1},
                    'Bristol Depot': {'time': 0, 'error': 1},
                    'Parson St': {'time': 0, 'error': 1},
                    'Fishponds': {'time': 0, 'error': 1}}
        over40 = {}
        over200 = {}

    for key in airquality.AREAS:
        # if (time.time() - air_data[key]['time']) > (15 * 60):
        air_data[key] = airquality.get_air_dict(key, True)
        if air_data[key]['NO215m'] > airquality.NO2YLM:
            over40[key] = air_data[key]['NO215m']
        if air_data[key]['NO224h'] > airquality.NO215LM:
            over200[key] = air_data[key]['NO224h']
        error = air_data[key]['error']

    get_data.air_data = air_data
    get_data.over40 = over40
    get_data.over200 = over200

    print("Error status: " + str(error))
    return air_data, over40, over200, error


def get_zero_data():
    air_data = {}
    over40 = {}
    over200 = {}
    error = 1

    for key in airquality.AREAS:
        air_data[key] = airquality.get_zeros()

    return air_data, over40, over200, error


@app.route("/")
def choking():
    # [air_data, over40, over200, err] = get_data()
    [air_data, over40, over200, err] = get_zero_data()

    return render_template('index.html', airdata=air_data, url=[airquality.URL, airquality.SITEURL], urlcodes=airquality.AREAS,  areas=over40.keys(), choking=len(over40), time=time.time(), over200=over200, error=err)

@socketio.on('ready')
def scrape_data():
    print('Page loaded')
    [air_data, over40, over200, err] = get_data()
    names = list(airquality.AREAS)
    over40 = list(over40.keys())
    # print(over40)
    over200 = list(over200.keys())
    emit('data_loaded', {'air_data': air_data, 'areas': names, 'over40': over40, 'over200': over200, 'time': time.time(), 'choking': len(over40), 'error': err})

with app.test_request_context():
    url_for('static', filename='style.css')

if __name__ == '__main__':
    socketio.run(app)
