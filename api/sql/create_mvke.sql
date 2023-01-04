DROP TABLE IF EXISTS mvke;

CREATE TABLE mvke (
    'MATNR'	varchar(30),
    'VKORG'	varchar(15),
    'BONUS'	varchar(15),
    'VMSTA'	varchar(15),
    'VMSTD'	varchar(15),
    'MTPOS'	varchar(15),
    'DWERK'	varchar(15),
    'MVGR4'	varchar(15),
    'PRAT1'	varchar(15),
    'PRAT8'	varchar(15),
    'PRAT4'	varchar(15),
    'MVGR2' varchar(15),

  PRIMARY KEY (
    'VKORG', 'MATNR'
  )
);