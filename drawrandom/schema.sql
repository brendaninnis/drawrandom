DROP TABLE IF EXISTS list;
DROP TABLE IF EXISTS item;

CREATE TABLE list (
  key TEXT PRIMARY KEY
);

CREATE TABLE item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  list TEXT NOT NULL,
  name TEXT NOT NULL,
  assignee TEXT,
  FOREIGN KEY (list) REFERENCES list (key)
);
