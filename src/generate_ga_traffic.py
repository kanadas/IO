import sys
import requests
from send_requests_api import send
from constants import WRONG_DATA, OK, CONNECTION_PROBLEM, EMPTY_OPTION, WAIT_NEW_SENDING, WAIT_CONTINUE_SENDING,\
    STOP_SENDING


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


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Wrong parameters number.\nUsage: python generate_ga_traffic.py tracking_id url visits_no time.")
    else:
        tracking_id = sys.argv[1]
        url = sys.argv[2]
        visits_no = int(sys.argv[3])
        time = int(sys.argv[4])
        sending = True
        all_sent = 0

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
                print("Connection problem.")
                sending, option = decide()
