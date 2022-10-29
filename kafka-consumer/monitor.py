import json
import time

from Database.db import RedisDB

from .utils.common import get_consumer, start_prometheus
from .utils.constants import MessageType
from .utils.message_parser import parse_message

start_prometheus()

# wait for 5 seconds to make sure all services are ready
time.sleep(5)

db = RedisDB()
consumer = get_consumer()

print("Listening for Kafka messages...")


def process_message(message):
    if message is None:
        return
    try:
        text = message.value.decode("utf-8")
    except Exception:
        text = message

    parsed_message = parse_message(text)
    if parsed_message is None:
        return

    if parsed_message[0] == MessageType.RECOMMEND:
        userId = "".join(parsed_message[1])
        movie_list = ",".join(parsed_message[2:])
        value = json.dumps(
            {
                "movies": movie_list,
                "created_time": time.time(),
            }
        )
        db_key = "rec:" + userId
        db.set(db_key, value)
        return

    if parsed_message[0] == MessageType.WATCHTIME:
        userId = parsed_message[2]
        db_key = "rec:" + userId
        value = db.get(db_key)
        if value is not None:
            value = json.loads(value)
            recommended_movies = value["movies"].split(",")
            movieId = parsed_message[3]
            if movieId in recommended_movies:
                # increment the count for watched recommended movies
                db.execute_command("TS.INCRBY", "rec:watched:counter", 1)

                # add the time difference between the recommendation and the watchtime
                time_diff = time.time() - value["created_time"]
                db.execute_command("TS.ADD", "rec:watched:after", "*", time_diff)

                # add the rank of the movie in the recommendation list
                movie_index = recommended_movies.index(movieId) + 1
                rank = 1 / movie_index
                db.execute_command("TS.ADD", "rec:watched:rank", "*", rank)

                # remove the recommendation from the list of stored recommendations
                new_recommendations = recommended_movies
                new_recommendations[movie_index] = " " # replace the movieId with a space
                value["movies"] = ",".join(new_recommendations)
                db.set(db_key, json.dumps(value))

                print("logged watched")


for message in consumer:
    try:
        process_message(message)
    except Exception as e:
        print("[ERROR]", e)
