import json
import time

from Database.db import RedisDB

from .cloud_database import con, gtl, pmfc
from .utils.common import get_consumer, start_prometheus
from .utils.constants import APP_MODE, MessageType
from .utils.message_parser import parse_message

start_prometheus()

db = RedisDB()
consumer = get_consumer()

print("Listening for Kafka messages...")


def getAppModeFromUID(uid):
    """Find which app mode (canary or main) was used to generate the latest recommendations
    for the user. Returns 'canary' for Canary app, or 'main' for Main app recommendations."""
    try:
        # get data from recommendations cache
        main_data = db.get(uid)
        canary_data = db.get(APP_MODE.CANARY + ":" + uid)
        if canary_data is not None and main_data is not None:
            canary_data = json.loads(canary_data)
            main_data = json.loads(main_data)
            if "timestamp" in canary_data and "timestamp" in main_data:
                if float(canary_data["timestamp"]) > float(main_data["timestamp"]):
                    return APP_MODE.CANARY
                else:
                    return APP_MODE.MAIN
            elif "timestamp" in canary_data:
                return APP_MODE.CANARY
            else:
                return APP_MODE.MAIN
        elif canary_data is not None:
            return APP_MODE.CANARY
        else:
            return APP_MODE.MAIN
    except Exception as e:
        print("Error getting app mode from uid: ", e)
        return APP_MODE.MAIN


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
                "app_mode": getAppModeFromUID(userId),
            }
        )
        db_key = "rec:" + userId
        db.set(db_key, value)
        return

    elif parsed_message[0] == MessageType.BROKEN:
        db.execute_command("TS.ADD", "rec:failed:counter", "*", 1)

    elif parsed_message[0] == MessageType.WATCHTIME:
        userId = parsed_message[2]
        db_key = "rec:" + userId
        value = db.get(db_key)
        if value is not None:
            value = json.loads(value)
            recommended_movies = value["movies"].split(",")
            db_key_prefix = ""
            if "app_mode" in value and value["app_mode"] == APP_MODE.CANARY:
                db_key_prefix = APP_MODE.CANARY + ":"

            movieId = parsed_message[3]
            if movieId in recommended_movies:
                # increment the count for watched recommended movies
                db.execute_command(
                    "TS.INCRBY", db_key_prefix + "rec:watched:counter", 1
                )

                # add the time difference between the recommendation and the watchtime
                time_diff = time.time() - value["created_time"]
                db.execute_command(
                    "TS.ADD", db_key_prefix + "rec:watched:after", "*", time_diff
                )

                # add the rank of the movie in the recommendation list
                movie_index = recommended_movies.index(movieId) + 1
                rank = 1 / movie_index
                db.execute_command(
                    "TS.ADD", db_key_prefix + "rec:watched:rank", "*", rank
                )

                # remove the recommendation from the list of stored recommendations
                new_recommendations = recommended_movies
                new_recommendations[
                    movie_index
                ] = "#"  # replace the movieId with a # symbol
                value["movies"] = ",".join(new_recommendations)
                db.set(db_key, json.dumps(value))


supabase = con()
count_watch = 0
count_rating = 0
threshold = 100000

protect_rating = 0

for message in consumer:
    try:
        process_message(message)
        if not db.connected_to_redis:
            db.connect()
    except Exception as e:
        print("[ERROR]", e)

    # upload logs to database stuff
    try:
        if count_rating <= threshold:
            count_rating += pmfc(supabase, message, "RATING")
            print("rating:", count_rating)

        if count_watch <= threshold and protect_rating > 50:
            count_watch += pmfc(supabase, message, "WATCHTIME")
            print("watchtime:", count_watch)

        # check if the database is cleaned
        if count_watch >= threshold and protect_rating > 50:
            current_size = gtl(supabase, "WatchTime")
            if current_size < 10:
                count_watch = current_size
                print("databse is clean, reset watch counter")

        if count_rating >= threshold and protect_rating % 50:
            current_size = gtl(supabase, "Rating")
            if current_size < 10:
                count_rating = current_size
                print("databse is clean, reset rating counter")

        protect_rating += 1

        if protect_rating > 55:
            protect_rating = 0

    except Exception as e:
        print("[ERROR]", e)
