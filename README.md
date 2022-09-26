# Team-3

Code for our project. Please try to update this document as we add more features/changes.

## Installation

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
