import time

from pykafka import KafkaClient
from utils.constants import MessageType
from utils.message_parser import parse_message

HOST = "fall2022-comp585.cs.mcgill.ca:9092"  # HOST to connect to
TOPIC = "movielog3"  # Topic to read from

client = KafkaClient(hosts=HOST)
topic = client.topics[TOPIC]
consumer = topic.get_simple_consumer()
print("Connected to Kafka host: ", HOST)
print("Reading from topic: ", TOPIC)


# MessageType.RATING or MessageType.WATCHTIME
def readKafkaStream(streamType: MessageType, numberOfLogs: int):
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
            text = message.value.decode("utf-8")
            parsed_message = parse_message(text)

            # currently, we will encounter recommendation log, but it will give error:
            # Invalid message:  ['2022-09-27T02:33:53.863', '276020', 'recommendation request fall2022-comp585-3.cs.mcgill.ca:8082', ' status 0',
            # ' result: java.net.ConnectException: connection timed out: fall2022-comp585-3.cs.mcgill.ca/132.206.51.206:8082', ' 818 ms']
            # Therefore, use try block to avoid None result.
            try:
                message_type = parsed_message[2]
            except Exception:
                message_type = MessageType.RECOMMEND

            if message_type != streamType:
                continue
            # print(parse_message(text))

            time_stamp, user, type, movieId, rating_minute = parse_message(text)

            if streamType == MessageType.RATING:
                # If reading rating,
                # directly insert new row to the dataframe
                # df.loc[len(df.index)] = [user, movieId, rating_minute]
                line = str(user) + "," + str(movieId) + "," + str(rating_minute) + "\n"
                data_file.write(line)
            else:

                # set up threshold
                if int(rating_minute) >= 10:
                    # df.loc[len(df.index)] = [user, movieId, rating_minute]
                    line = (
                        str(user) + "," + str(movieId) + "," + str(rating_minute) + "\n"
                    )
                    data_file.write(line)
                else:
                    count -= 1  # to compensate the log that is filtered out.

            count += 1
            if count % 1000 == 0:
                print("----------------------------------------------")
                print(count, " / ", numberOfLogs)
                end = time.time()
                print("Total time consumed (in sec): ", (end - start))
                print("----------------------------------------------")
            if count >= numberOfLogs:
                break
    data_file.close()

    # df.to_csv (r'data.csv', index = False, header=True)


readKafkaStream(MessageType.WATCHTIME, 100000)

# count = 0
# start = time.time()
# for message in consumer:
#     if message is not None:
#         text = message.value.decode('utf-8')
#         parsed_message = parse_message(text)

#         try:
#             message_type = parsed_message[2]
#         except:
#             message_type = MessageType.RECOMMEND

#         if message_type != TYPE_STEAM:
#             continue
#         #print(parse_message(text))

#         time_stamp, user, type, movieId, rating_minute = parse_message(text)
#         df.loc[len(df.index)] = [user, movieId, rating_minute]          # insert new row to the dataframe

#         count += 1
#         if count % 100 == 0:
#             print(count, " / ", LIMIT)
#             end = time.time()
#             print("time consumed from start:", end - start)
#         if count >= LIMIT:
#             break

# df.to_csv (r'data.csv', index = False, header=True)
