import json
from enum import Enum


class APP_MODES(Enum):
    CANARY = "canary"
    MAIN = "main"


# inteface for saved recommendation data
class SavedRec:
    def __init__(self, str_data=None):
        if str_data is None:
            return
        # parse data into json
        try:
            data = json.loads(str_data)

            self.userID = data.get("userID")
            self.recommendations = data.get("recommendations")
            self.timestamp = data.get("timestamp")
            self.sha = data.get("sha")
            self.app_mode = data.get("app_mode")
        except Exception as e:
            print("Could not parse data: " + str(e))

    def init(self, userID, recommendations, timestamp, sha, app_mode):
        self.userID = userID
        self.recommendations = recommendations
        self.timestamp = timestamp
        self.sha = sha
        self.app_mode = app_mode

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return self.toJSON()
