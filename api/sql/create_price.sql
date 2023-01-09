DROP TABLE IF EXISTS price;

CREATE TABLE price (
    vkorg TEXT,
    matnr TEXT,
    valid_to TEXT,
    valid_from TEXT,
    amount TEXT,
    uom	TEXT,
    per_unit TEXT,
    prat1	TEXT,
    prat8	TEXT,
    prat4	TEXT,
    mvgr2 TEXT,
  PRIMARY KEY (
    vkorg, matnr
  )
);