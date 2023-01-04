DROP TABLE IF EXISTS sales_text;

CREATE TABLE sales_text (
    'Material' varchar(30),
    'Sales Organisation' varchar(10),
    'Language' varchar(10),
    'Existing Sales Text'	varchar(255),
    'Modified Sales Text' varchar(255),
  PRIMARY KEY (
    'Sales Organisation', 'Material'
  )
);