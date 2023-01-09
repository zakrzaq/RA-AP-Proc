DROP TABLE IF EXISTS sales_text;

CREATE TABLE sales_text (
    matnr TEXT,
    vkorg TEXT,
    lang TEXT,
    sales_text TEXT,
    new_text TEXT,
  PRIMARY KEY (
    vkorg, matnr
  )
);