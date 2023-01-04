DROP TABLE IF EXISTS ausp;

CREATE TABLE ausp (
    'OBJEK'	varchar(30),
    'ATINN'	varchar(50),
    'KLART'	varchar(10),
    'ATWRT' varchar(20),
  PRIMARY KEY (
    'ATINN', "OBJEK"
  )
);