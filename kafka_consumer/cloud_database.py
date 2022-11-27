from supabase import create_client

# from .utils.constants import MessageType
# from .utils.message_parser import parse_message

# table: Rating or WatchTime
# data in json format
# data = {
#     'userId' : 'alex',
#     'movieId' : 'cat+and+we',
#     'rating' : 2
# }


def parse_message_local(message):
    """Parses a message from Kafka and returns a tuple of the message type and the"""
    message = message.split(",")

    if len(message) == 3:
        # GET messages
        time = message[0]
        user = message[1]

        try:
            userID = user
            if not userID.isdigit():
                raise Exception
        except Exception:
            return ["BROKEN"]

        if "GET /rate/" in message[2]:
            type = "RATING"
            movieId = "+"
            rating = 0
            try:
                movieId = message[2].split("=")[0].split("/")[-1]
                rating = int(message[2].split("=")[1])
                # some logs are corrupted
                # ValueError: invalid literal for int() with base 10: ‘E’
            except Exception:
                type = "BROKEN"
                movieId = "-1"
                rating = -1
            return [type, time, user, movieId, rating]

        else:
            type = "WATCHTIME"
            minute = 0
            movieId = 0
            try:
                movieId = message[2].split("/")[3]
                minute = int(message[2].split("/")[4].split(".")[0])
                # sometimes this int() casting will fail
                # ‘GET /data/m/the+tulse+luper+suitcases_+part+1+the+moab+story+2003/6x1.mpg’]
            except Exception:
                type = "BROKEN"
                minute = -1
            return [type, time, user, movieId, minute]
    elif len(message) == 25:
        # recommendation messages tested and it will be 25.
        type = "RECOMMEND"
        recommendation = []
        tokens = []
        for m in message:
            tokens.append(m.replace(" ", ""))  # remove space in between

        tokens[4] = tokens[4].replace(
            "result:", ""
        )  # first movie recommendation will start with "result:"
        recommendation.append(type)

        try:
            userID = tokens[1]
            if not userID.isdigit():
                raise Exception
        except Exception:
            return ["BROKEN"]

        recommendation.append(tokens[1])
        recommendation = recommendation + tokens[4:24]
        return recommendation
    else:
        return ["BROKEN"]


def insert_data(database, table, data):
    try:
        database.table(table).insert(data).execute()  # inserting one record
        return 1
    except Exception as e:
        print("insertion failed" + table)
        print(e)
        print("-" * 50)
        return 0


# the data parameter is useless in the input
def get_all_data(database, table, data):
    try:
        data = (
            database.table(table).select("*").execute()
        )  # select everything from the table
        print("get all data")
        return data
    except Exception:
        print("get all data failed")


# delete all data in a table
def delete_all_data(database, table):
    try:
        database.table(table).delete().eq("flag", 1).execute()
    except Exception:
        print("delete failed")


# connect to database
def con():
    API_URL = "https://lsfcmdyggefxunujmnxs.supabase.co"
    key1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxzZmNtZHlnZ2VmeHVudWptbnhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njg0NDczMjYs"
    key2 = "ImV4cCI6MTk4NDAyMzMyNn0.bY-L6ccfEGUK3pc2EeR-EnkWLQTzGvHGskMxXn1f4Uc"
    API_KEY = key1 + key2

    supabase = create_client(API_URL, API_KEY)
    return supabase


# process_message_for_cloud
def pmfc(database, message, type):
    if message is None:
        return 0
    try:
        text = message.value.decode("utf-8")
    except Exception:
        text = message

    parsed_message = parse_message_local(text)
    if parsed_message is None:
        return 0

    elif parsed_message[0] == "BROKEN":
        return 0

    elif parsed_message[0] == "RATING" and type == "RATING":
        type, time_stamp, user, movieId, rating_minute = parse_message_local(text)

        data = {
            "userId": user,
            "movieId": movieId,
            "rating": int(rating_minute),
        }
        try:
            insert_data(database, "Rating", data)
            return 1
        except Exception:
            return 0

    elif parsed_message[0] == "WATCHTIME" and type == "WATCHTIME":
        type, time_stamp, user, movieId, rating_minute = parse_message_local(text)
        # set up threshold
        if int(rating_minute) >= 10:
            data = {
                "userId": user,
                "movieId": movieId,
                "watchTime": int(rating_minute),
            }
            try:
                insert_data(database, "WatchTime", data)
                return 1
            except Exception:
                return 0

        else:
            return 0
    else:
        return 0


# get_table_length
def gtl(database, table):
    data = database.table(table).select("*").execute()
    # Assert we pulled real data.
    return len(data.data)


# # WATCHTIME OR RATING
# def getKafkaLogs(database, streamType, numberOfLogs: int, consumer):

#     count = 0

#     for message in consumer:

#         if message is not None:
#             try:
#                 text = message.value.decode(
#                     "utf-8"
#                 )  # if it is real log, it will go here
#             except Exception:
#                 # if it is mock log, it is already string
#                 text = message.replace("\n", "")

#             # data_file.write(text + "\n")

#             parsed_message = parse_message_local(text)

#             message_type = parsed_message[0]

#             if streamType == "RATING" and message_type == streamType:
#                 type, time_stamp, user, movieId, rating_minute = parse_message(text)

#                 # directly insert to the database
#                 data = {
#                     "userId": user,
#                     "movieId": movieId,
#                     "rating": int(rating_minute),
#                 }

#                 insert_data(database, "Rating", data)

#                 count += 1
#             elif streamType == "WATCHTIME" and message_type == streamType:
#                 type, time_stamp, user, movieId, rating_minute = parse_message(text)
#                 # set up threshold
#                 if int(rating_minute) >= 10:
#                     data = {
#                         "userId": user,
#                         "movieId": movieId,
#                         "watchTime": int(rating_minute),
#                     }
#                     insert_data(database, "WatchTime", data)

#                     count += 1
#             else:
#                 pass

#         if count >= numberOfLogs:
#             print("reading logs: " + str(numberOfLogs) + " is done")
#             break

# Example
# consumer = utils.common.get_consumer()
# getKafkaLogs(supabase, MessageType.WATCHTIME, 10, consumer)
# getKafkaLogs(supabase, MessageType.RATING, 10, consumer)

# delete_all_data(supabase, "WatchTime")

# supabase = connection()

# delete_all_data(supabase, "WatchTime")
# delete_all_data(supabase, "Rating")

# consumer = utils.common.get_consumer()
# count_watch = 0
# count_rating = 0
# threshold = 100

# s = time.time()
# getKafkaLogs(supabase, MessageType.RATING, 2000, consumer)
# e = time.time()
# print(e-s)
# exit()


# for message in consumer:

#     try:

#         if count_rating <= threshold:
#             count_rating += process_message_for_cloud(supabase, message, MessageType.RATING)
#             print("rating:", count_rating)

#         if count_watch <= threshold:
#             count_watch += process_message_for_cloud(supabase, message, MessageType.WATCHTIME)
#             print("watchtime:", count_watch)

#         # check if the database is cleaned
#         if count_watch >= threshold:
#             current_size = get_table_length(supabase, "WatchTime")
#             if current_size < 10:
#                 count_watch = current_size
#                 print("databse is clean, reset watch counter")

#         if count_rating >= threshold:
#             current_size = get_table_length(supabase, "Rating")
#             if current_size < 10:
#                 count_rating = current_size
#                 print("databse is clean, reset rating counter")

#         if count_watch >= threshold and count_rating >= threshold:
#             break

#     except Exception as e:
#         print("[ERROR]", e)


# print("count")
# start_time = time.time()
# x = get_table_length(supabase, "WatchTime")
# end = time.time()
# print(x)
# print(end-start_time)
