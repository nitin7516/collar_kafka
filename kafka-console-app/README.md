# IBM Event Streams and python producer/consumer application

This is the Python application which connect to [IBM Event Streams ], send and receive messages using the [confluent-kafka-python] library. It creates and list topics using the Event Streams for IBM Cloud Admin REST API.

## Running the application

### Prerequisites

* [Python](https://www.python.org/downloads/) 3.6 or later
* [IBM Event Streams ]
* [IBM Cloud foundry ]

### Installing dependencies

Run the following commands on your local machine, after the prerequisites for your environment have been completed:

```bash
pip install -r requirements.txt
```

### Supply IBM Event Streams credentials

Copy the `env.sample` file to `.env`.
Edit the `.env` file with IBM Event Streams credentials.
To find the values for `KAFKA_BROKERS_SASL`, `KAFK_ADMIN_URL` and `PASSWORD`, access your Event Streams instance in IBM Cloud®, go to the `Service Credentials` tab and select the `Credentials` you want to use.

### Running the application

### Flask producer

After login into the IBM cloud navigate to the cloud shell.
Under the directory execute  the command : 
```bash
git clone https://github.com/chhabrabhishek/collar_kafka.git 
```
Navigate to folder cd collor_kafka/kafka_console_app and then execute: 
```bash
cp env.sample .env
```
Execute command: 
```bash
ibmcloud cf push producer (it will create a cloud foundary service for python flask app)
```
After running console will display an access URL for the producer.
 e.g http://producer-quick-crocodile-ah.eu-gb.mybluemix.net/produce?lat=123.45.67.777&long=355.66.24.6&temp=50 for producing.
 
if required to check the recent logs we can execute:
```bash
ibmcloud cf logs producer --recent
```
Once we have produced the data the topic, now we can see our data can be consumed by a kafka consumer.
To run kafaka consumer, execute the following command:
```bash
pip install -r requirements.txt
```
Once requirements are installed , execute the following command:

```bash
python3 consumer.py
```

The sample will run indefinitely until interrupted. To stop the process, use `Ctrl+C`.
