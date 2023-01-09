DROP TABLE IF EXISTS mvke;

CREATE TABLE mvke (
    matnr	text,
    vkorg	text,
    bonus	text,
    vmsta	text,
    vmstd	text,
    mtpos	text,
    dwerk	text,
    mvgr4	text,
    prat1	text,
    prat8	text,
    prat4	text,
    mvgr2 text,

  PRIMARY KEY (
    vkorg, matnr
  )
);