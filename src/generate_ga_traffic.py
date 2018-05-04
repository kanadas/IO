import sys
from send_requests_api import send
from constants import WRONG_DATA, OK, CONNECTION_PROBLEM


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Wrong parameters number.\nUsage: python generate_ga_traffic.py tracking_id url vists_no time.")
    else:
        result = send(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

        if result == OK:
            print("Successfully send users.")
        elif result == WRONG_DATA:
            print("Tracking_id is wrong.")
        else: #CONNECTION_PROBLEM
            pass