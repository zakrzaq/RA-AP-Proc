DROP TABLE IF EXISTS marc;

CREATE TABLE marc (
    'MATNR'	 varchar(30),
    'WERKS'	varchar(15),
    'MMSTA'	varchar(15),
    'DISPO'	varchar(15),
    'DISMM'	varchar(15),
    'INDUS'	varchar(15),
    'STEUC'	varchar(15),
    'ORG_SOURCE_VAL' varchar(15),
    'BESKZ'	varchar(15),
    'PSTAT' varchar(15),
  PRIMARY KEY (
    'WERKS', 'MATNR'
  )
);