import requests
import random
from math import floor, ceil
import uuid
import time
from constants import WRONG_DATA, OK, CONNECTION_PROBLEM
from users import generate_users


def check_data(tracking_id, url):
    try:
        response = requests.post("https://www.google-analytics.com/debug/collect", data={
            "tid": tracking_id,
            "dp": url,
            "v": 1,
            "cid": 1
        }, timeout=60)
    except (requests.Timeout, requests.ConnectionError):
        return False, CONNECTION_PROBLEM

    if response.json()["hitParsingResult"][0]["valid"]:
        return True, OK
    else:
        return False, WRONG_DATA


def generate_data(visits_no):
    return generate_users(visits_no)


def send(tracking_id, url, visits_no, sending_time):
    correct, result = check_data(tracking_id, url)

    if correct:
        data = generate_data(visits_no)
        batch_size = len(data) // sending_time
        ak = 0;
        for i in range(sending_time):
            num = random.randint(floor((len(data) - ak) / (sending_time - i) / 1.5), ceil((len(data) - ak) / (sending_time - i) * 1.5))
            if i == sending_time - 1: num = len(data) - ak
            for id, user in enumerate(data[ak : ak + num]):
                try:
                    requests.post("https://www.google-analytics.com/collect", data={
                        "v": 1,
                        "tid": tracking_id,
                        "cid": user.cid,
                        "dp": url,
                        "ua": user.agent,
                        "geoid": user.geoid
                    }, timeout=60)
                except (requests.Timeout, requests.ConnectionError):
                    return CONNECTION_PROBLEM, id

            ak += num
            while time.clock() % 1 > 0.01:
                pass
            #time.sleep(1)

        return OK, visits_no
    else:
        return result, 0

