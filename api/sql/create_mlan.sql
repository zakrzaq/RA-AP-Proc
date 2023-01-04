DROP TABLE IF EXISTS mlan;

CREATE TABLE mlan (
    'MANDT'	varchar(5),
    'MATNR'	varchar(30),
    'ALAND'	varchar(6),
    'TAXM1'	varchar(6),
    'TAXM2'	varchar(6),
    'TAXM3'	varchar(6),
    'TAXM4'	varchar(6),
    'TAXM5'	varchar(6),
    'TAXM6'	varchar(6),
    'TAXM7'	varchar(6),
    'TAXM8'	varchar(6),
    'TAXM9'	varchar(6),
    'TAXIM' varchar(6),
  PRIMARY KEY (
    'ALAND', 'MATNR'
  )
);