from sap.se16 import se16
from sap.gts import gts
from sap.ih09 import ih09
from sap.sqvi import sqvi
from sap.text import text

tables = ["MARC", "MVKE", "AUSP", "MLAN"]

text()
ih09()
for t in tables:
    se16(t)
sqvi()
gts()
