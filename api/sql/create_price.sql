DROP TABLE IF EXISTS price;

CREATE TABLE price (
    'SOrg.' varchar(6),
    'Material' varchar(30),
    'Valid to' varchar(20),
    'Valid From' varchar(20),
    'Amount' varchar(30),
    'UoM'	varchar(10),
    'per Unit' varchar(10),
    'PRAT1'	varchar(10),
    'PRAT8'	varchar(10),
    'PRAT4'	varchar(10),
    'MVGR2' varchar(10),
  PRIMARY KEY (
    'SOrg.', 'Material'
  )
);