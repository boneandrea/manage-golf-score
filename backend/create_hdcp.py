from datetime import datetime
import sys
from util import *
from database import *
"""
docker compose exec backend python /home/create_hdcp.py
"""


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
            try:
                for member in game["scores"]:
                    members.append(member["name"])
            except KeyError:
                continue

        for name in sorted(list(set(members))):
            user = {"name": name, "hdcp": 0}
            print(user)
            db["members"].insert_one(user)

    def default_query(self):
        return {
            "date":
            {
                "$gte": datetime(2023, 1, 1),
                "$lt": datetime(2025, 1, 1)
            }
        }

    def create_members(self):
        games = self.collect_members()


if __name__ == "__main__":

    x = CreateHdcp(verbose=True)
    x.create_members()
