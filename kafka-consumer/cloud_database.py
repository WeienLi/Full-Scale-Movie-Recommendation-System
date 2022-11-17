import psycopg2
from supabase import create_client
from utils.constants import MessageType
from utils.message_parser import parse_message


# table: Rating or WatchTime
# data in json format
# data = {
#     'userId' : 'alex',
#     'movieId' : 'cat+and+we',
#     'rating' : 2
# }
def insert_data(database, table, data):
    try:
        database.table(table).insert(data).execute()  # inserting one record
    except:
        print("insertion failed")


def get_all_data(database, table, data):
    try:
        data = (
            database.table(table).select("*").execute()
        )  # select everything from the table
        print("get all data")
        return data
    except:
        print("get all data failed")


# Todo
# idea: add a dummy column to as flag. Only have value 1.
#       When we need to delete a table, we use: supabase.table("countries").delete().eq("flag", 1).execute()
def delete_all_data(database, table):
    try:
        database.table(table).delete().eq("flag", 1).execute()
    except:
        print("delete failed")


def getKafkaLogs(database, streamType: MessageType, numberOfLogs: int, consumer):

    count = 0

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

                # directly insert to the database
                data = {
                    "userId": user,
                    "movieId": movieId,
                    "rating": int(rating_minute),
                }

                insert_data(database, "Rating", data)

                count += 1
            elif streamType == MessageType.WATCHTIME and message_type == streamType:
                type, time_stamp, user, movieId, rating_minute = parse_message(text)
                # set up threshold
                if int(rating_minute) >= 10:
                    data = {
                        "userId": user,
                        "movieId": movieId,
                        "watchTime": int(rating_minute),
                    }
                    insert_data(database, "WatchTime", data)

                    count += 1
            else:
                pass

        if count >= numberOfLogs:
            print("reading logs: " + str(numberOfLogs) + " is done")
            break


# connect to database
API_URL = "https://lsfcmdyggefxunujmnxs.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxzZmNtZHlnZ2VmeHVudWptbnhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njg0NDczMjYsImV4cCI6MTk4NDAyMzMyNn0.bY-L6ccfEGUK3pc2EeR-EnkWLQTzGvHGskMxXn1f4Uc"
supabase = create_client(API_URL, API_KEY)
supabase

# consumer = get_consumer()
# getKafkaLogs(supabase, MessageType.WATCHTIME, 10, consumer)
# getKafkaLogs(supabase, MessageType.RATING, 10, consumer)

# delete_all_data(supabase, "WatchTime")


conn = psycopg2.connect(
    database="postgres",
    host="db.lsfcmdyggefxunujmnxs.supabase.co",
    user="postgres",
    password="gE9A9MvnPFYwdwD",
    port="5432",
)
print("connection")
cursor = conn.cursor()
result = cursor.execute('SELECT * FROM "WatchTime"')
print(result)
