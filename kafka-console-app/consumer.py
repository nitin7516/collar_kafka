import asyncio
import os
import signal
import sys

import consumertask
import rest

from dotenv import load_dotenv

class EventStreamsSample(object):

    def __init__(self):
        self.opts = {}
        self.run_consumer = True
        self.consumer = None

        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        self.opts['brokers'] = os.getenv("KAFKA_BROKERS_SASL")
        self.opts['rest_endpoint'] = os.getenv("KAFKA_HTTP_URL")
        self.opts['api_key'] = os.getenv("PASSWORD")
        self.opts['username'] = os.getenv("USER")
        self.opts['topic_name'] = os.getenv("TOPIC")

        print('Kafka Endpoints: {0}'.format(self.opts['brokers']))
        print('Admin REST Endpoint: {0}'.format(self.opts['rest_endpoint']))
        print('API_KEY: {0}'.format(self.opts['api_key']))

        if any(k not in self.opts for k in ('brokers', 'rest_endpoint', 'api_key')):
            print('Error - Failed to retrieve options. Check that app is bound to an Event Streams service or that command line options are correct.')
            sys.exit(-1)

        # Use Event Streams' REST admin API to create the topic
        # with 1 partition and a retention period of 24 hours.
        rest_client = rest.EventStreamsRest(self.opts['rest_endpoint'], self.opts['api_key'])
        print('Creating the topic {0} with Admin REST API'.format(self.opts['topic_name']))
        response = rest_client.create_topic(self.opts['topic_name'], 1, 24)
        print(response.text)

        # Use Event Streams' REST admin API to list the existing topics
        print('Admin REST Listing Topics:')
        response = rest_client.list_topics()
        print(response.text)

    def shutdown(self):
        print('Shutdown received.')
        if self.run_consumer:
            self.consumer.stop()

    async def run_tasks(self):
        driver_options = {
            'bootstrap.servers': self.opts['brokers'],
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': self.opts['username'],
            'sasl.password': self.opts['api_key'],
            'api.version.request': True,
            'broker.version.fallback': '0.10.2.1',
            'log.connection.close' : False
        }
        consumer_opts = {
            'client.id': 'kafka-python-console-sample-consumer',
            'group.id': 'kafka-python-console-sample-group'
        }

        # Add the common options to consumer and producer
        for key in driver_options:
            consumer_opts[key] = driver_options[key]

        tasks = []

        if self.run_consumer:
            self.consumer = consumertask.ConsumerTask(consumer_opts, self.opts['topic_name'])
            tasks.append(asyncio.ensure_future(self.consumer.run()))

        done, pending = await asyncio.wait(tasks)
        for future in done | pending:
            future.result()
        sys.exit(0)

if __name__ == "__main__":
    app = EventStreamsSample()
    signal.signal(signal.SIGINT, app.shutdown)
    signal.signal(signal.SIGTERM, app.shutdown)
    print('This sample app will run until interrupted.')
    sys.exit(asyncio.get_event_loop().run_until_complete(app.run_tasks()))