from multiprocessing import Process
from src.generate_ga_traffic import generate_ga_traffic
import sqlite3
import time

conn = sqlite3.connect('../Scheduler/instance/scheduler.sqlite')
cur = conn.cursor()
running_tasks = {}

while True:
    for row in cur.execute("SELECT task_id, tracking_id, url, visits, generating_time FROM task WHERE start_time <= datetime('now', 'localtime') AND state_name = 'READY'"):
        proc = Process(target=generate_ga_traffic, args= row[1:5])
        proc.start()
        running_tasks[row[0]] = proc
        cur.execute("UPDATE task SET state_name = 'IN_PROGRESS' WHERE task_id = ?", (str(row[0]),))
        print('Added task with id: %s tracking_id: %s, visits %s, and generating_time %s' % (str(row[0]), str(row[1]), str(row[3]), str(row[4])))

    for row in cur.execute("SELECT task_id FROM task WHERE state_name = 'CANCELED'"):
        if row[0] in running_tasks:
            running_tasks[row[0]].terminate()
            del running_tasks[row[0]]
            print('Canceled task with id: %s' % str(row[0]))

    items = list(running_tasks.items())
    for task_id, proc in items:
        if not proc.is_alive():
            status = 'ERROR'
            if proc.exitcode == 0:
                status = 'DONE'
            cur.execute("UPDATE task SET state_name = ? WHERE task_id = ?", (status, str(task_id)))
            del running_tasks[task_id]
            print('Removed task with id: %s and status %s' % (str(task_id), status))

    conn.commit()
    time.sleep(1)

