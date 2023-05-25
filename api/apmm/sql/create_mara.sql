DROP TABLE IF EXISTS mara;

CREATE TABLE mara (
    matnr TEXT,
    mtart TEXT,
    mat_description TEXT,
    cat_group TEXT,
    prod_hierarchy TEXT,
  PRIMARY KEY (
    matnr
  )
);