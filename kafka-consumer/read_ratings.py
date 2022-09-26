from pykafka import KafkaClient
from utils.constants import MessageType
from utils.message_parser import parse_message

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
        parsed_message = parse_message(text)
        message_type = parsed_message[2]
        if message_type != MessageType.RATING:
            continue
        print(parse_message(text))
        count += 1
        if count >= LIMIT:
            break