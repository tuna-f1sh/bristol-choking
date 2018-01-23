import airquality
from flask import Flask, url_for, render_template
app = Flask(__name__)


@app.route("/index")
def hello(name=None):
    return render_template('index.html', name=name)


@app.route("/")
def choking():
    i = 0
    air_data = [0] * len(airquality.AREAS)
    over = [0] * len(airquality.AREAS)

    for key in airquality.AREAS:
        air_data[i] = airquality.get_air_dict(key, True)
        if air_data[i]['NO215m'] > airquality.NO2YLM:
            print(air_data[i]['NO215m'])
            over[i] = 1
        i += 1

    string = '<h1>data</h1>'
    for v in over:
        if v is 1:
            string += '<h1>Yes</h1>'
        else:
            string += '<h1>No</h1>'
    #for n, v in air_data[0].items():
        #string += n + ': '
        #string += str(v) + '<br/>'

    return string


with app.test_request_context():
    url_for('static', filename='style.css')
