DROP TABLE IF EXISTS state;
DROP TABLE IF EXISTS task;

CREATE TABLE state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE task (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id TEXT NOT NULL,
    url TEXT NOT NULL,
    generating_time INTEGER NOT NULL,
    state_name TEXT NOT NULL,
    visits INTEGER NOT NULL,
    start_time  DATE NOT NULL,
    FOREIGN KEY (state_name) REFERENCES state (id)
);
