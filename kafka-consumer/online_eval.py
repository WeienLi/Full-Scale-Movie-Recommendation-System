import time
from xmlrpc.client import boolean

from pykafka import KafkaClient
from pykafka.common import OffsetType
from utils.constants import MessageType
from utils.message_parser import parse_message


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


# --------------------------------------------
#       Helper methods
# --------------------------------------------

# index = int id
# user = userid
# movie_list = list of recommended movie
# create_time = when the checking starts
# time_spam = whehter checking is done
class recommendation:
    def __init__(
        self,
        index: int,
        user,
        movie_list: list,
        created_time,
        time_spam_finished: boolean = False,
    ):
        self.index = index
        self.user = user
        self.movies = movie_list
        self.created_time = created_time
        self.time_spam_finished = time_spam_finished
        self.watch_movie = []


#  find index of a recommendtion request with userID
def findRecommendationIdFromUserId(userId, recommendation_list: list[recommendation]):
    output_list = []
    for rec in recommendation_list:
        # check if the time spam has passed
        if (userId == rec.user) and (rec.time_spam_finished is False):
            output_list.append(rec)

    return output_list


# create file name with recommendation index
def fileNameByIndex(index: int):
    file = "online_eval_data/" + str(index) + ".csv"
    return file


# end the evaluation process if all rec has done collecting info.
def shouldEndEval(recommendations_list: list[recommendation], data_files, time_span):

    nonFinished = 0

    for rec in recommendations_list:
        current_time = time.time()
        # this time spam is done
        if (rec.time_spam_finished) is False and (
            current_time - rec.created_time > time_span
        ):
            file = data_files[rec.index]
            file.close()
            rec.time_spam_finished = True
            print("time spam finsihed")

        if rec.time_spam_finished is False:
            nonFinished = nonFinished + 1

    # print(str(nonFinished) + " // " + str(len(rec_list)))

    # if nonFinished == 0 => every one is done
    # we should end evaluation
    # if not,
    # someone is unfinished, continue.
    return nonFinished == 0


# ------------------------------------------------------------------
#              Main program start here
# ------------------------------------------------------------------

# ----------------------
#     Workflow
# ----------------------

# The workflow is that:
# record recommendation request
# distribute following watchtime logs into corresponding files w.r.t recommendation request
# this is done by recommendation index

# TODO use the watchtime logs to calcualte the matrics
# TODO whehther we need to set up a db

# input:
# num of recommendation requests to evaluate
# time spam for each recommendation to be evaluated within, in seconds e.g. 3600 for reading 1 hour


def get_recommendation_request_feedback(num_recommendation, time_span, consumer):
    recommendatins = (
        []
    )  # store recommendation instance, each object is a recommendation request
    recommendatin_index = (
        0  # index of recommendation request. Help to store infomation into file i/o
    )
    data_files = []  # store list of opened file

    timer_time = time.time()  # help to indiate executing time
    timer = 0  # same as the above one

    for message in consumer:
        if message is not None:
            try:
                text = message.value.decode("utf-8")
            except Exception:
                text = message

            parsed_message = parse_message(text)

            if parsed_message is not None:

                # create recommendation object and store in the list
                if (parsed_message[0] == MessageType.RECOMMEND) and (
                    recommendatin_index < num_recommendation
                ):
                    current_t = time.time()
                    rec = recommendation(
                        index=recommendatin_index,
                        user=parsed_message[1],
                        movie_list=parsed_message[2:],
                        created_time=current_t,
                    )
                    recommendatins.append(rec)

                    file = fileNameByIndex(recommendatin_index)
                    data_file = open(file, "w")
                    data_files.append(data_file)
                    recommendatin_index += 1
                    print("add recommendation!")

                # add watchtime log to corresponding local file.
                if parsed_message[0] == MessageType.WATCHTIME:
                    userId = parsed_message[2]
                    recommendations = findRecommendationIdFromUserId(
                        userId, recommendatins
                    )
                    for rec in recommendations:

                        rec.watch_movie.append(parsed_message[3])

                        # file = data_files[index]
                        # min = parsed_message[4]

                        # line = (
                        #     + parsed_message[3]
                        #     + ","
                        #     + str(min)
                        #     + "\n"
                        # )
                        # file.write(line)

                        print("add movie")

                # indicate executing time so that only print only for each sec
                # print every 2 sec
                processing_time = time.time()
                if (processing_time - timer_time) > timer:
                    timer = timer + 2
                    print(str(processing_time - timer_time) + " sec has passed")
                    print(len(recommendatins))
                    print("--------------/ separate / ----------------")

                # end for loop if all recommendation request has done collecting logs. i.e. time-spam is done
                if (
                    shouldEndEval(recommendatins, data_files, time_span)
                    and len(recommendatins) == num_recommendation
                ):
                    break

    return recommendatins


# give a recommendation list
# calcuate MRR for each recommendation
# MRR info: https://en.wikipedia.org/wiki/Mean_reciprocal_rank


def calculate_MRR(recommendations_list: list[recommendation]):
    accpet_rates = []
    for rec in recommendations_list:

        rec.movies
        unique_rec_movie = []

        for i in rec.movies:
            # Add to the new list
            # only if not present
            if i not in unique_rec_movie:
                unique_rec_movie.append(i)

        unique_watch_movie = []
        for i in rec.watch_movie:
            # Add to the new list
            # only if not present
            if i not in unique_watch_movie:
                unique_watch_movie.append(i)

        Q = len(unique_watch_movie)
        MRR = 0.0
        for watch_movie in unique_watch_movie:
            try:
                rank = unique_rec_movie.index(watch_movie)
                rank = rank + 1
                MRR = MRR + 1 / rank
            except Exception:
                rank = 0

        MRR = MRR / Q
        accpet_rates.append(MRR)

    return accpet_rates


# consumer = get_consumer()
# consumer = [
#     "2047,2223,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
#     "2047,1234,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
#     "2047,2211,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
#     "2022-10-07T14:21:02,2223,GET /data/m/+in+/17.mpg",
#     "2022-10-07T14:21:02,2223,GET /data/m/a/17.mpg",
#     "2022-10-07T14:21:02,2223,GET /data/m/+v/17.mpg",
#     "2022-10-07T14:21:02,1234,GET /data/m/+v/17.mpg",
#     "2022-10-07T14:21:02,1234,GET /data/m/e+v+1988/17.mpg",
#     "2022-10-07T14:21:02,1234,GET /data/m/w+1/17.mpg",
#     "2022-10-07T14:21:02,2211,GET /data/m/+v/17.mpg",
#     "2022-10-07T14:21:02,2211,GET /data/m/e+v+1988/17.mpg",
#     "2022-10-07T14:21:02,2211,GET /data/m/w+1/17.mpg",
#     "2022-10-07T14:21:02,2211,GET /data/m/in+a++w+2010/17.mpg",
# ]
# rec_list = get_recommendation_request_feedback(3, 10, consumer)
# for rec in rec_list:
#     print(rec.user)
#     print(len(rec.watch_movie))

# accpet_rates = calculate_MRR(rec_list)
# for r in accpet_rates:
#     print(r)
