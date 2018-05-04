import requests
from constants import WRONG_DATA, OK


def check_data(tracking_id, url):
    response = requests.post("https://www.google-analytics.com/debug/collect",
                             data={"tid": tracking_id, "dp": url, "v": 1, "cid": 1})

    if response.json()["hitParsingResult"][0]["valid"]:
        return True
    else:
        return False


def generate_data(visits_no):
    pass


def send(tracking_id, url, visits_no, time):
    result = check_data(tracking_id, url)

    if result:
        data = generate_data(visits_no)
        return OK
    else:
        return WRONG_DATA

