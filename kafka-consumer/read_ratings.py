from pykafka import KafkaClient

HOST = 'fall2022-comp585.cs.mcgill.ca:9092' # HOST to connect to
TOPIC = 'movielog3'                         # Topic to read from
LIMIT = 100                                 # Number of messages to read


client = KafkaClient(hosts=HOST)
topic = client.topics[TOPIC]
consumer = topic.get_simple_consumer()
print("Connected to Kafka host: ", HOST)
print("Reading from topic: ", TOPIC)

count = 0
for message in consumer:
    if message is not None:
        text = message.value.decode('utf-8')
        print(text)
        count += 1
        if count >= LIMIT:
            break