DROP TABLE IF EXISTS log;

CREATE TABLE log (
    date_added TEXT,
    target_sorg TEXT,
    target_plant TEXT,
    email_prefix TEXT,
    matnr TEXT,
    service TEXT,
    location TEXT,
    catalog TEXT,
    mtart TEXT,
    us_dchain TEXT,
    us_cs TEXT,
    rason TEXT,
    comment TEXT,
    legacy_matnr TEXT,
    active INTEGER,
  PRIMARY KEY (
    target_sorg, matnr
  )
);

