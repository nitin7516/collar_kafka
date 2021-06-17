## Kafka streaming application using IBM Streams

Our application is built using IBM Streams and Apache Kafka service.
we will be using `IBM Event Streams` on IBM Cloud, which is a high-throughput message bus built on the Kafka platform. 
Kafka producer is deployed on IBM cloud foundry.


## Featured technologies

* [Python](https://www.python.org/): Python is a programming language that lets you work more quickly and integrate your systems more effectively.
* [Event Streams]
  > **NOTE**: Python 3 is required for this application to run locally.

## Prerequisites

* An [IBM Cloud Account](https://cloud.ibm.com)

## Steps

1. [Clone the repo](#1-clone-the-repo)
1. [Provison Event Streams on IBM Cloud](#2-provison-event-streams-on-ibm-cloud)
1. [Create sample Kafka console python app](#3-create-sample-kafka-console-python-app)

### 1. Clone the repo

```bash
git clone https://github.com/IBM/ibm-streams-with-kafka
```

### 2. Provison Event Streams on IBM Cloud

To create your IBM Event Streams service:

* From your IBM Cloud dashboard, click on `create resource`.
* Search the catalog for `streams`.
* Click the `Event Streams` tile to launch the create panel.

![event-streams-service](doc/source/images/event-streams-service.png)

From the panel, enter a unique name, a region and resource group, and a plan type (select the default `lite` plan). Click `Create` to create and enable your service.

#### Launch Event Streams

From the IBM Cloud dashboard, click on your new Event Streams service in the resource list.

#### Create Event Streams topic

From the `Manage` tab panel of your Event Streams service, click `Topics`.

From the `Topics` panel, click the `Create topic +` button.

![event-streams-manage](doc/source/images/event-streams-manage.png)

From the `Create Topics` panel, enter the name `clicks` for the topic name. Then click `Next`.

![event-streams-topic](doc/source/images/event-streams-topic.png)

In the subsequent panels, accept the default values of 1 partition and 1 retention day.

>**NOTE**: Under the `lite` plan, you will only be able to create one topic.

#### Collect service credentials

In order to remotely connect to your new Event Streams service, you will need generate service credentials.

From the `Service credentials` tab panel, click the `New Credentials` button. The credential values we will be using include:

* **kafka_brokers_sasl**
* **kafka_http_url**
* **password**
* **user**

![event-streams-creds](doc/source/images/event-streams-creds.png)

### 3. Create sample Kafka console python app

Your `Event Streams` service panel provides a `Getting started` panel that links to a repository of sample apps you can use to send and receive `Event Stream` messages. The sample shows how a producer sends messages to a consumer using a `topic`. The same sample program is used to consume messages and produce messages.

For convenience, the python version of the sample app is included in this repo and is located in the `/kafka-console-app` directory. The code has also been slightly modified to work better with this code pattern.

For a full list and descriptions of the available sample `Event Streams` apps, visit [https://github.com/ibm-messaging/event-streams-samples](https://github.com/ibm-messaging/event-streams-samples).

#### Building the app

To build the sample app:

```bash
cd kafka-console
pip install -r requirements.txt
cp env.sample .env
```

Edit the `.env` file in the local directory and update the values to match the credentials you created in the previous step.

>**NOTE**: Formatting of text in the `.env` file is very strict. When cutting/pasting the `kafka_brokers_sasl` values, ensure that you remove all quote marks and internal spaces. Also, you should not have to change the default `username` and `topic name` values if you followed the previous steps for setting up your `Event Streams` service.

The Kafka console app has 2 modes it can run in: `producer` or `consumer`. The mode is set using run-time arguments.

#### Running the app

To run the app, use the following command:

```bash
python3 app.py -producer
# OR
python3 app.py -consumer
```

In `producer` mode, test messages are sent to the Kafka service with the topic name set to `clicks`. Each message will be printed to the console.

In `consumer` mode, a Kafka service reader is set up to listen for message where the topic name is set to `clicks`. Each message received will be printed to the console.

To test the app, start a producer in one terminal console, and a consumer in a separate terminal console.



