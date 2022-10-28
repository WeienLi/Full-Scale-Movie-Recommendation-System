import os

import redis


class RedisDB:
    def __init__(self):
        try:
            REDIS_HOST = os.getenv("REDIS_HOST")
            REDIS_PORT = os.getenv("REDIS_PORT")
            self.r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
            )
            if self.r.ping():
                print("Connected to Redis")
        except Exception as e:
            self.r = None
            self.r_local = {}
            print(str(e) + ".\nUsing dynamic dictionary instead.")

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
