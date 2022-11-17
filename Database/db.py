import os

import redis


class RedisDB:
    def __init__(self):
        try:
            self.connect()
        except Exception as e:
            self.r = None
            self.r_local = {}
            print(str(e) + ".\nUsing dynamic dictionary instead.")

    def connect(self):
        """Connect to Redis"""
        self.connected_to_redis = False
        REDIS_HOST = os.getenv("REDIS_HOST")
        REDIS_PORT = os.getenv("REDIS_PORT")
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,)
        if self.r.ping():
            print("Connected to Redis")
            self.connected_to_redis = True
            self.save_local_files_to_redis()
        else:
            raise Exception("Could not connect to Redis")

    def save_local_files_to_redis(self):
        """Save the local (temporary) dictionary to Redis"""
        try:
            for key, value in self.r_local.items():
                self.r.set(key, value)
            self.r_local = {}
        except Exception as e:
            print("Could not save local files to Redis: " + str(e))

    def get(self, key):
        """Get the (string) value of a key"""
        if self.r is not None:
            return self.r.get(key)
        else:
            if key in self.r_local:
                return self.r_local[key]
        return None

    def set(self, key, value):
        """Set the (string) value of a key"""
        if self.r is not None:
            self.r.set(key, value)
        else:
            self.r_local[key] = value

    def incr(self, key):
        """Increment the value of a key"""
        if self.r is not None:
            return self.r.incr(key)
        else:
            cur_val = 0
            if key in self.r_local:
                cur_val = int(self.r_local[key])
            self.r_local[key] = str(cur_val + 1)
            return self.r_local[key]

    def execute_command(self, command, *args):
        """Execute a Redis command"""
        if self.r is not None:
            return self.r.execute_command(command, *args)
        else:
            print("Cannot execute command without Redis")
            return None
