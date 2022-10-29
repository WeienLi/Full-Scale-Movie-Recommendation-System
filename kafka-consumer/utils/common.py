from pykafka import KafkaClient
from pykafka.common import OffsetType


# get a new Kafka consumer
def get_consumer():
    HOST = "fall2022-comp585.cs.mcgill.ca:9092"  # HOST to connect to
    TOPIC = "movielog3"  # Topic to read from
    client = KafkaClient(hosts=HOST)
    topic = client.topics[TOPIC]

    print("online evaluation!")
    print("Connected to Kafka host: ", HOST)
    print("Reading from topic: ", TOPIC)

    # this consumer config guarantees that it reads latest logs every time
    consumer = topic.get_simple_consumer(
        auto_offset_reset=OffsetType.LATEST, reset_offset_on_start=True
    )
    return consumer
