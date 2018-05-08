import requests
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

        for id, user in enumerate(data):
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
            time.sleep(sending_time / visits_no)

        return OK, visits_no
    else:
        return result, 0

