# Team-3

Code for our project. Please try to update this document as we add more features/changes.

## Installation (Skip this part if running with docker)

```
pip install -r requirements.txt
```

Keep requirements.txt up to date if you install some new packages:

```
pip freeze > requirements.txt
```

## Running kafka-consumer

🟥 IMPORTANT: You'll need to be on the McGill network (Wifi or VPN) to access the Kafka streams.

#### Read user ratings

```
python kafka-consumer/read_ratings.py
```

## Running flask_API

The recommender API can be run inside a Docker container. A utility script (`docker.sh`) can help you easily manage the server.

#### Prerequisites

Docker must be installed on the machine ([Download Docker](https://docs.docker.com/get-docker/)).
(Linux/MacOS) Make the utility script executable:

```
chmod +x docker.sh
```

#### Starting the server

Starts the Flask API server in the background inside a Docker container.

```
./docker.sh start
```

#### Accessing the API

See the API in action by going to `http://<ip-of-the-virtual-machine>:8082`:

- **http://127.0.0.1:8082/** - If you're running this locally. Otherwise, you may need to port forward if you're running the API on a remote machine.
- **http://fall2022-comp585-3.cs.mcgill.ca:8082/** - If you're running the API on our team's remote server. NOTE: You'll need to be on McGill VPN to access this.

#### Stopping the server

Stops all running Docker instances of the Flask API server.

```
./docker.sh stop
```

#### Loading the ALS model

To the load the ALS model make sure the folder is approriatedly downloaded and DO NOT ZIP, zip will loses metadata of the model.

Import neccessary dependency to load the model

```
from pyspark.ml.recommendation import ALSModel
```

Loading

```
[varname] = ALSModel.load("[path]/ALS")
```
