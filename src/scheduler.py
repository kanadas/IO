from multiprocessing import Process
from generate_ga_traffic import generate_ga_traffic
import sqlite3

conn = sqlite3.connect('../Scheduler/instance/scheduler.sqlite')
cur = conn.cursor()
running_tasks = {}

while(True):
    for row in cur.execute("SELECT task_id, tracking_id, url, visits, generating_time FROM task WHERE start_time <= datetime('now') AND state_name = 'READY'"):
        proc = Process(target=generate_ga_traffic, args= row[1:4])
        proc.start()
        running_tasks[row[0]] = proc
        cur.execute("UPDATE task SET status = 'IN_PROGRESS' WHERE task_id = ?", row[0])

    for row in cur.execute("SELECT task_id FROM task WHERE state = CANCELED"):
        if row[0] in running_tasks:
            running_tasks[row[0]].terminate()
            del running_tasks[row[0]]

    for task_id, proc in running_tasks.items():
        if not proc.is_alive():
            if proc.exitcode == 0:
                status = 'DONE'
            else:
                status = 'ERROR'
        cur.execute("UPDATE task SET status = ? WHERE task_id = ?", status, task_id)
        del running_tasks[task_id]


