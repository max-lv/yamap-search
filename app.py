#!/usr/bin/python
from flask import Flask, request, render_template, escape
import requests as req
import json
import hashlib
import re
import os


# Yandex.maps API key
APIKEY = '<YOUR API KEY HERE>'
# What we're searching for
SEARCH = 'Газпромнефть'
# Where we're store saved requests
CSV_PATH = './tmp/'


app = Flask(__name__)


def save_request(city, data):
    # get somewhat unique id using hashing
    h = hashlib.sha256()
    h.update(city.encode('utf8'))
    
    file_name = h.hexdigest()[:10]

    # save file
    with open( CSV_PATH + file_name, 'w') as f:
        f.write(json.dumps(data))

    return file_name



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/')
def api():
    response = {}

    try:
        city = request.args['city']
        city = escape(city)

        payload = {
            'text': '{}, {}'.format(SEARCH, city), # ie. 'Газпромнефть, Москва'
            'results': 1000,
            'type': 'biz',
            'lang': 'ru_RU',
            'apikey': APIKEY
        }
        r = req.get('https://search-maps.yandex.ru/v1/', params=payload)

        if r.status_code == 200:
            # filter out unwanted data
            j = json.loads(r._content)
            data = []
            for el in j['features']:
                data.append({
                    'id': el['properties']['CompanyMetaData']['id'],
                    'address': el['properties']['CompanyMetaData']['address'],
                    'coordinates': el['geometry']['coordinates']
                })

            file_id = save_request(city, data)

            response = {
                'success': True,
                'data': data[:5],
                'total': len(data),
                'file_id': file_id
            }
        else:
            response = {
                'success': False,
                'error': 'There was some error requesting data.'
            }
    except KeyError:
        response = {
            'success': False,
            'error': 'Please supply `city` parameter.'
        }

    return json.dumps(response)



@app.route('/csv/<file_name>')
def csv(file_name):
    # filter user input.
    file_name = re.sub(r'([^a-zA-Z0-9]+)', '', file_name)

    # Read in file with saved json from request
    with open(CSV_PATH + file_name,'r') as f:
        data = json.loads(f.read())

    # Parse json to csv
    csv = 'id;Долгота;Широта;Адрес'
    for el in data:
        csv = csv + '\n' + ';'.join([
            el['id'],
            str(el['coordinates'][0]),
            str(el['coordinates'][1]),
            el['address']
        ])

    return (csv, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="gps_points.csv"',
        'Content-Description': 'File Transfer',
        'Content-Length': len(csv)
    })



if __name__ == '__main__':
    # Creating directory for storing CSVs
    if not os.path.exists(CSV_PATH):
        os.makedirs(CSV_PATH)

    app.run()