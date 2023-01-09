DROP TABLE IF EXISTS marc;

CREATE TABLE marc (
    matnr TEXT,
    werks TEXT,
    mmsta TEXT,
    dispo TEXT,
    dismm TEXT,
    indus TEXT,
    steuc TEXT,
    org_source TEXT,
    nezkz TEXT,
    pstat TEXT,
  PRIMARY KEY (
    werks, matnr
  )
);