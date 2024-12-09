from datetime import datetime
import sys
from util import *
from database import *


class CreateHdcp:
    db = None

    def __init__(self, verbose):
        self.verbose = verbose

    def log(self, *msg):
        if self.verbose:
            print(*msg)

    def collect_members(self, query={}):
        client = database().connect_db()
        db = client["score"]
        table = db["score"]
        members = []
        for game in table.find():
            for member in game["scores"]:
                members.append(member["name"])
                print({"name": member["name"], "hdcp": 0})

        return sorted(list(set(members)))

    def default_query(self):
        return {
            "date":
            {
                "$gte": datetime(2023, 1, 1),
                "$lt": datetime(2025, 1, 1)
            }
        }

    def set_best_gross(self):
        games = self.collect_members()


if __name__ == "__main__":

    x = CreateHdcp(verbose=True)
    x.set_best_gross()
