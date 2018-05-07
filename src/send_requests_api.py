import requests
import uuid
import time
from constants import WRONG_DATA, OK, CONNECTION_PROBLEM


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


#to narazie zeby sprawdzic czy dziala
def generate_data(visits_no):
    return [{"agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.1"} for _ in range(visits_no)]


def send(tracking_id, url, visits_no, sending_time):
    correct, result = check_data(tracking_id, url)

    if correct:
        data = generate_data(visits_no)
        batch_size = len(data) // sending_time

        for i in range(sending_time):
            for id, user in enumerate(data[i:i + batch_size]):
                try:
                    requests.post("https://www.google-analytics.com/collect", data = {
                        "v": 1,
                        "tid": tracking_id,
                        "cid": uuid.uuid4(),
                        "dp": url,
                        "ua": user["agent"] # nie wiem jak beda wygenerowani uzytkownicy
                    }, timeout=60)
                except (requests.Timeout, requests.ConnectionError):
                    return CONNECTION_PROBLEM, i * batch_size + 1 + id, i + 1
            time.sleep(1)

        return OK, visits_no, sending_time
    else:
        return result, 0, 0

