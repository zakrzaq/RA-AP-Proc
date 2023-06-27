import os
from utils.data_frames import get_selected_active, get_selected_archive
import pandas as pd
from utils.helpers import use_dotenv

use_dotenv()
active = get_selected_active()
archive = get_selected_archive()

matnrs = ["PN-55851"]

target_sorgs = []

f = open("test.txt", "w")
for line in archive.columns:
    line = f'"{line}"'
f.write("; ".join(archive.columns))  # type: ignore
f.close()

if len(target_sorgs) < 1:
    active_result = active[active["SAP MATNR\n(from request form)"].isin(matnrs)]
    archive_result = archive[archive["SAP MATNR\n(from request form)"].isin(matnrs)]
else:
    active_result = active[active["SAP MATNR\n(from request form)"].isin(matnrs)]
    archive_result = archive[archive["SAP MATNR\n(from request form)"].isin(matnrs)]

active_result = active_result[
    [
        "Date Added",
        "target sorg",
        "target plant",
        "email prefix\n(from request form)",
        "SAP MATNR\n(from request form)",
        "Service Requested\n(from request form)",
        " sorg1k dchain",
        " sorg1k cs",
        "target sorg dchain",
        "target sorg DWERK",
        "target sorg cs",
        "target sorg pub",
        "target plant status",
        "target plant mrp type",
        "DWERK Plant Status",
        "status",
    ]
]
archive_result = archive_result[
    [
        "Date Added",
        "target sorg",
        "target plant",
        "email prefix\n(from request form)",
        "SAP MATNR\n(from request form)",
        "Service Requested\n(from request form)",
        " sorg1k dchain",
        " sorg1k cs",
        "target sorg dchain",
        "target sorg DWERK",
        "target sorg cs",
        "target sorg pub",
        "target plant status",
        "target plant mrp type",
        "DWERK Plant Status",
        "status",
    ]
]

print(active_result)
print(archive_result)

writer = pd.ExcelWriter(
    os.path.join(os.environ["DIR_OUT"], "_QUERY.xlsx"), engine="xlsxwriter"
)
active_result.to_excel(writer, sheet_name="ACTIVE", index=False)
archive_result.to_excel(writer, sheet_name="ARCHIVE", index=False)
writer.close()
