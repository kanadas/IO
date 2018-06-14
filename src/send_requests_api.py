# Request sending API.

import requests
import random
from math import floor, ceil
import time
from .constants import WRONG_DATA, OK, CONNECTION_PROBLEM
from .users import generate_users


# Main function sending the requests.
def send(tracking_id, url, visits_no, sending_time):
    data = generate_users(visits_no)
    counter = 0;

    # Sending the requested amount of users per minute.
    for i in range(sending_time):
        num = random.randint(floor((len(data) - counter) / (sending_time - i) / 1.5),
                             ceil((len(data) - counter) / (sending_time - i) * 1.5))
        if i == sending_time - 1:
            num = len(data) - counter
        for id, user in enumerate(data[counter : counter + num]):
            try:
                # Sending the request.
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

        counter += num
        while time.clock() % 1 > 0.01:
            pass

    return OK, visits_no

