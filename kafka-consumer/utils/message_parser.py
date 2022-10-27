from utils.constants import MessageType


def parse_message(message):
    """Parses a message from Kafka and returns a tuple of the message type and the"""
    message = message.split(",")

    if len(message) == 3:
        # GET messages
        time = message[0]
        user = message[1]
        if "GET /rate/" in message[2]:
            type = MessageType.RATING
            movieId = "+"
            rating = 0
            try:
                movieId = message[2].split("=")[0].split("/")[-1]
                rating = int(message[2].split("=")[1])
                # some logs are corrupted
                # ValueError: invalid literal for int() with base 10: ‘E’
            except Exception:
                type = MessageType.BROKEN
            return [type, time, user, movieId, rating]

        else:
            type = MessageType.WATCHTIME
            minute = 0
            movieId = 0
            try:
                movieId = message[2].split("/")[3]
                minute = int(message[2].split("/")[4].split(".")[0])
                # sometimes this int() casting will fail
                # ‘GET /data/m/the+tulse+luper+suitcases_+part+1+the+moab+story+2003/6x1.mpg’]
            except Exception:
                type = MessageType.BROKEN
            return [type, time, user, movieId, minute]
    elif len(message) == 25:
        # recommendation messages tested and it will be 25.
        type = MessageType.RECOMMEND
        recommendation = []
        tokens = []
        for m in message:
            tokens.append(m.replace(" ", ""))  # remove space in between

        tokens[4] = tokens[4].replace(
            "result:", ""
        )  # first movie recommendation will start with "result:"
        recommendation.append(type)
        recommendation.append(tokens[1])
        recommendation = recommendation + tokens[4:24]
        return recommendation
    else:
        return [MessageType.BROKEN]
