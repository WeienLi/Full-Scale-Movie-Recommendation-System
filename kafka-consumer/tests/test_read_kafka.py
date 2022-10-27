import sys

from read_Kafka import readKafkaStream
from utils.constants import MessageType

sys.path.append("..")


def test_read_kafka():
    print("test_read_kafka")
    assert True


def test_readKafkaStream():
    print("test_readKafkaStream")
    try:
        print("mocked logs")
        file = open("mock_logs.csv", "r")
        consumer = file.readlines()
        readKafkaStream(MessageType.RATING, 1000, consumer)
        readKafkaStream(MessageType.WATCHTIME, 1000, consumer)
        assert True
    except Exception as e:
        print(e)
        assert False
