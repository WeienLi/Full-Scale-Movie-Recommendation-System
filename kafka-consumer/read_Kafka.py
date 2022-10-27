import time

from utils.constants import MessageType
from utils.message_parser import parse_message

# comment out for unit test purpose
# in real production, please uncomment this

# try:
#     HOST = "fall2022-comp585.cs.mcgill.ca:9092"  # HOST to connect to
#     TOPIC = "movielog3"  # Topic to read from
#     client = KafkaClient(hosts=HOST)
#     topic = client.topics[TOPIC]
#     consumer = topic.get_simple_consumer()
#     print("Connected to Kafka host: ", HOST)
#     print("Reading from topic: ", TOPIC)
# except Exception as e:
#     print(e)
#     print("mocked logs")
#     file = open("mock_logs.csv", "r")
#     consumer = file.readlines()


# MessageType.RATING or MessageType.WATCHTIME
def readKafkaStream(streamType: MessageType, numberOfLogs: int, consumer):

    start = time.time()
    if streamType == MessageType.RATING:
        ratingOrWatchtime = "rating"
    else:
        ratingOrWatchtime = "watchTime"

    # template = {"userID":[],"movieID":[],ratingOrWatchtime:[]}
    # df = pd.DataFrame(template)

    count = 0

    # clear data_file first and then append
    data_file = open("data.csv", "w")
    column = "userID,movieID," + ratingOrWatchtime + "\n"
    data_file.write(column)
    data_file.close()

    data_file = open("data.csv", "a")
    for message in consumer:

        if message is not None:
            try:
                text = message.value.decode(
                    "utf-8"
                )  # if it is real log, it will go here
            except Exception:
                # if it is mock log, it is already string
                text = message.replace("\n", "")

            # data_file.write(text + "\n")

            parsed_message = parse_message(text)

            message_type = parsed_message[0]

            if streamType == MessageType.RATING and message_type == streamType:
                type, time_stamp, user, movieId, rating_minute = parse_message(text)
                # If reading rating,
                # directly insert new row to the dataframe
                # df.loc[len(df.index)] = [user, movieId, rating_minute]
                line = str(user) + "," + str(movieId) + "," + str(rating_minute) + "\n"
                data_file.write(line)
                count += 1
            elif streamType == MessageType.WATCHTIME and message_type == streamType:
                type, time_stamp, user, movieId, rating_minute = parse_message(text)
                # set up threshold
                if int(rating_minute) >= 10:
                    # df.loc[len(df.index)] = [user, movieId, rating_minute]
                    line = (
                        str(user) + "," + str(movieId) + "," + str(rating_minute) + "\n"
                    )
                    data_file.write(line)
                    count += 1
            else:
                pass

            if count % 100 == 0:
                print("----------------------------------------------")
                print(count, " / ", numberOfLogs)
                end = time.time()
                print("Total time consumed (in sec): ", (end - start))
                print("----------------------------------------------")

            if count >= numberOfLogs:
                print("reading logs: " + str(numberOfLogs) + " is done")
                break
    data_file.close()

    # df.to_csv (r'data.csv', index = False, header=True)


# readKafkaStream(MessageType.RATING, 10, consumer)
