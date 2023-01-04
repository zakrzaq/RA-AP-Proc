DROP TABLE IF EXISTS mara;

CREATE TABLE mara (
    'Material' varchar(30),
    'Material Type' varchar(5),
    'Material Description' varchar(150),
    'Gen. item cat. grp' varchar(10),
    'Product hierarchy' varchar(50),
  PRIMARY KEY (
    'Material'
  )
);