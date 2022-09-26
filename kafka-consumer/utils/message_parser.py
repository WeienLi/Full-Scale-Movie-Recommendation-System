from utils.constants import MessageType

def parse_message(message):
    '''Parses a message from Kafka and returns a tuple of the message type and the'''
    message = message.split(',')
    if len(message) == 3:
        ## GET messages
        time = message[0]
        user = message[1]
        if 'GET /rate/' in message[2]:    
            type = MessageType.RATING
            movieId = message[2].split('=')[0].split('/')[-1]
            rating = int(message[2].split('=')[1])
            return [time, user, type, movieId, rating]
        else:
            type = MessageType.WATCHTIME
            movieId = message[2].split('/')[3]
            minute = int(message[2].split('/')[4].split('.')[0])
            return [time, user, type, movieId, minute]
    elif len(message) == 4:
        ## recommendation messages
        # TODO: Implement this
        return []
    else:
        print("Invalid message: ", message)
        return None

