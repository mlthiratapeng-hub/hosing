import json
import os

PATH = "data/rank_data.json"

def load():

    if not os.path.exists(PATH):

        with open(PATH,"w") as f:
            json.dump({},f)

    with open(PATH,"r") as f:
        return json.load(f)


def save(data):

    with open(PATH,"w") as f:
        json.dump(data,f,indent=4)