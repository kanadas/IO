from .send_requests_api import send
from .constants import OK, MAX_REQUESTS_PER_MINUTE


def check_if_proper_number(num, msg):
    is_int = True
    try:
        num_int = int(num)
        if num_int < 0:
            print("Only positive number of %s! %d" % (msg, num_int))
            is_int = False
    except ValueError:
        is_int = False
        print("%s has to be an integer!" % msg)
    return is_int


def generate_ga_traffic(tracking_id, url, visits_no, time):
    sending = True
    all_sent = 0

    if visits_no / time > MAX_REQUESTS_PER_MINUTE:
        print("We can't generate so much visits in that time")
        exit(1)

    while sending:
        result, sent_users = send(tracking_id, url, visits_no - all_sent, time)
        all_sent += sent_users

        if result == OK:
            sending = False
            print("Successfully sent %d/%d users." % (all_sent, visits_no))
        else: # CONNECTION_PROBLEM
            print("Connection problem.")
            exit(2)
