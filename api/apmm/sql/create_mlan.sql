DROP TABLE IF EXISTS mlan;

CREATE TABLE mlan (
    mandt TEXT,
    matnr TEXT,
    aland TEXT,
    taxm1 TEXT,
    taxm2 TEXT,
    taxm3 TEXT,
    taxm4 TEXT,
    taxm5 TEXT,
    taxm6 TEXT,
    taxm7 TEXT,
    taxm8 TEXT,
    taxm9 TEXT,
    taxim TEXT,
  PRIMARY KEY (
    aland, matnr
  )
);