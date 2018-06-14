# The main script for Task sending.

from .send_requests_api import send
from .constants import OK, MAX_REQUESTS_PER_MINUTE


def generate_ga_traffic(tracking_id, url, visits_no, time):
    sending = True
    all_sent = 0

    # Loop sending the requests.
    while sending:
        result, sent_users = send(tracking_id, url, visits_no - all_sent, time)
        all_sent += sent_users

        if result == OK:
            sending = False
            print("Successfully sent %d/%d users." % (all_sent, visits_no))
        else: # CONNECTION_PROBLEM
            print("Connection problem.")
            exit(2)
