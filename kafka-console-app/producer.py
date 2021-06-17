import os
import sys

import producertask
import rest

from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/produce")
def hello_world():
    opts = {}
    run_producer = True
    producer = None
    geo_coordinates = {
        'Latitude': request.args['lat'],
        'Longitude': request.args['long'],
        'Temperature': request.args['temp']
    }

    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    opts['brokers'] = os.getenv("KAFKA_BROKERS_SASL")
    opts['rest_endpoint'] = os.getenv("KAFKA_HTTP_URL")
    opts['api_key'] = os.getenv("PASSWORD")
    opts['username'] = os.getenv("USER")
    opts['topic_name'] = os.getenv("TOPIC")

    if any(k not in opts for k in ('brokers', 'rest_endpoint', 'api_key')):
        print('Error - Failed to retrieve options. Check that app is bound to an Event Streams service or that command line options are correct.')
        sys.exit(-1)
    
    rest_client = rest.EventStreamsRest(opts['rest_endpoint'], opts['api_key'])
    rest_client.create_topic(opts['topic_name'], 1, 24)

    run_tasks(opts, run_producer, producer, geo_coordinates)

    return "Success"

def run_tasks(opts, run_producer, producer, geo_coordinates):
    driver_options = {
        'bootstrap.servers': opts['brokers'],
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': opts['username'],
        'sasl.password': opts['api_key'],
        'api.version.request': True,
        'broker.version.fallback': '0.10.2.1',
        'log.connection.close' : False
    }
    producer_opts = {
        'client.id': 'kafka-python-console-sample-producer',
    }

    for key in driver_options:
        producer_opts[key] = driver_options[key]

    if run_producer:
        producer = producertask.ProducerTask(producer_opts, opts['topic_name'])
        producer.run(geo_coordinates)

app.run()
