#!/usr/bin/python

from flask import Flask, render_template, jsonify, request, send_file
from flask_bootstrap import Bootstrap
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
from utils import read_papers, read_acm
from location import geo_data, collab_data, get_countries_data

# APP
app = Flask(__name__)
Bootstrap(app)

# Static path
static_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))


@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/papers')
@app.route('/papers/')
def papers():

    # Get papers
    papers = read_papers()

    return render_template('papers.html', papers = papers)


@app.route('/acm')
@app.route('/acm/')
def acm():

    # Get ACM info
    acm = read_acm()

    return render_template('acm.html', papers = acm)


@app.route('/collaborations')
@app.route('/collaborations/')
def collaborations():

    return render_template('collaborations.html')


@app.route('/geodata')
@app.route('/geodata/')
def geodata():
    """ Get MAP's marks """

    return dumps(geo_data())


@app.route('/collabdata')
@app.route('/collabdata/')
def collabdata():
    """ Get MAP's collaborations """

    return dumps(collab_data())


@app.route('/countries')
def countries():
    """ Get countries """

    return render_template('countries.html')


@app.route('/countriesdata')
@app.route('/countriesdata/')
def countriesdata():
    """ Get MAP's countries """

    return dumps(get_countries_data())


@app.route('/map/icon')
def icon():
    """ Get ASU ICON """

    return send_file(os.path.join(static_path, 'logo.jpg'), mimetype='image/jpeg')


@app.route('/example')
def example():
    """ Example """

    return render_template('example.html')


@app.route('/another')
def map2():
    """ Another example """

    return render_template('another.html')


if __name__ == '__main__':
    
    app.run(host = '0.0.0.0', debug = True)