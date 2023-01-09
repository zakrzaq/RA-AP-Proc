DROP TABLE IF EXISTS ausp;

CREATE TABLE ausp (
    objek	TEXT,
    atinn	TEXT,
    klart	TEXT,
    atwrt TEXT,
  PRIMARY KEY (
    atinn, objek
  )
);