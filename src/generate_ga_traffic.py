import sys
import requests
from send_requests_api import send
from constants import WRONG_DATA, OK, CONNECTION_PROBLEM, EMPTY_OPTION, WAIT_NEW_SENDING, WAIT_CONTINUE_SENDING,\
    STOP_SENDING, MAX_REQUESTS_PER_MINUTE 


def internet_on():
    try:
        requests.get('http://216.58.192.142', timeout=1)
        return True
    except (requests.Timeout, requests.ConnectionError):
        return False


def decide():
    option = EMPTY_OPTION

    while not (option == WAIT_NEW_SENDING or option == WAIT_CONTINUE_SENDING or option == STOP_SENDING):
        option = int(input("Type:\n1 - Wait for connection and start new sending\n2 - Wait for connection and continue"
                           " sending\n3 - Stop sending\n"))

    if option == STOP_SENDING:
        return False, option
    else:
        while not internet_on():
            pass

        print("Connected.")

        return True, option


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
        elif result == WRONG_DATA:
            sending = False
            print("Tracking_id is wrong.")
        else: # CONNECTION_PROBLEM
            exit(2)
        #    print("Connection problem.")
        #    sending, option = decide()
    
