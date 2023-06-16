import os
import pandas as pd
from tqdm import tqdm

from helpers.helpers import use_dotenv
from helpers.ap_data_utils import get_cert, columns_names
from helpers.files import sap_data_files

use_dotenv()

mara = marc = mvke = ausp = mlan = gts = price = text = pd.DataFrame()
inputs = sap_data_files
dfs = {}


def read_data(name: str, path: str):
    df = (
        pd.read_excel(path)
        if ".XLSX" in path
        else pd.read_csv(path, sep="\t", encoding="utf-16")
    )
    df.name = name
    dfs[name] = df


for key, value in inputs.items():
    read_data(key, value)

# for name, df in dfs.items():
#     df.to_csv(os.path.join(os.environ["DIR_IN"], df.name + ".csv"))


def make_ap_data(parts_list=[]):
    parts = parts_list
    for part in tqdm(parts):
        cols = []
        date, sorg, plant, requestor, matnr, service, location = (
            part[0],
            int(part[1]),
            int(part[2]),
            part[3],
            part[4],
            part[5],
            part[6],
        )

        # logic
        cert = get_cert(sorg)

        # COLUMNS
        # legacy
        cols.append("")
        # duplicate
        cols.append(f"{sorg}{plant}{matnr}")
        # description
        dfs["mara"].loc[(dfs["mara"]["Material"] == matnr)]["Material Description"]
        # catalog
        cols.append(
            dfs["ausp"].loc[
                (dfs["ausp"]["OBJEK"] == matnr)
                & (dfs["ausp"]["ATINN"] == "CATALOG_STRING1"),
                ["ATWRT"],
            ]
        )
        # Series
        cols.append(
            dfs["ausp"].loc[
                (dfs["ausp"]["OBJEK"] == matnr)
                & (dfs["ausp"]["ATINN"] == "SERIES_DESIGNATOR"),
                ["ATWRT"],
            ]
        )
        # mtart
        cols.append(
            dfs["mara"].loc[(dfs["mara"]["Material"] == matnr)]["Material Type"]
        )
        #  sorg1k dchain
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == 1000),
                ["VMSTA"],
            ],
        )
        #  sorg1k cs
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == 1000),
                ["PRAT4"],
            ],
        )
        # sorg1k price
        cols.append(
            dfs["price"].loc[
                (dfs["price"]["Material"] == matnr) & (dfs["price"]["SOrg."] == 1000)
            ]["Amount"]
        )
        #  sorg4k dchain
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == 4000),
                ["VMSTA"],
            ],
        )
        #  sorg4k cs
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == 4000),
                ["PRAT4"],
            ],
        )
        # PGC
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == sorg),
                ["MVGR4"],
            ],
        )
        # target sorg price
        cols.append(
            dfs["price"].loc[
                (dfs["price"]["Material"] == matnr) & (dfs["price"]["SOrg."] == sorg)
            ]["Amount"]
        )
        # target sorg dchain
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == sorg),
                ["VMSTA"],
            ],
        )
        # target sorg DWERK
        dwerk = dfs["mvke"].loc[
            (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == sorg),
            ["DWERK"],
        ]
        cols.append("" if dwerk.empty else dwerk)
        dwerk = int(dwerk.values[0]) if not dwerk.empty else ""

        # target sorg cs
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == sorg),
                ["PRAT4"],
            ],
        )
        # target sorg pub
        cols.append(
            dfs["mvke"].loc[
                (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == sorg),
                ["PRAT4"],
            ],
        )
        # target plant status
        cols.append(
            dfs["marc"].loc[
                (dfs["marc"]["MATNR"] == matnr) & (dfs["marc"]["WERKS"] == plant),
                ["MMSTA"],
            ]
        )
        # target plant mrp type
        cols.append(
            dfs["marc"].loc[
                (dfs["marc"]["MATNR"] == matnr) & (dfs["marc"]["WERKS"] == plant),
                ["DISMM"],
            ]
        )
        # DWERK Plant Status
        if not isinstance(dwerk, str):
            cols.append(
                dfs["marc"].loc[
                    (dfs["marc"]["MATNR"] == matnr) & (dfs["marc"]["WERKS"] == dwerk),
                    ["MMSTA"],
                ]
            )
        else:
            cols.append("")
        # DWERK Plant Code
        if isinstance(dwerk, str):
            cols.append(
                dfs["marc"].loc[
                    (dfs["marc"]["MATNR"] == matnr) & (dfs["marc"]["WERKS"] == dwerk),
                    ["DISMM"],
                ]
            )
        else:
            cols.append("")
        # mif/soerf check
        plant_extended = dfs["marc"].loc[
            (dfs["marc"]["MATNR"] == matnr) & (dfs["marc"]["WERKS"] == plant)
        ]
        sorg_extended = dfs["mvke"].loc[
            (dfs["mvke"]["MATNR"] == matnr) & (dfs["mvke"]["VKORG"] == sorg),
            ["VMSTA"],
        ]
        if sorg_extended.empty or plant_extended.empty:
            cols.append("X")
        else:
            cols.append("")
        # sales text
        cols.append(
            dfs["text"].loc[
                (dfs["text"]["Material"] == matnr)
                & (dfs["text"]["Sales Organisation"] == sorg),
                ["Existing Sales Text"],
            ]
        )
        # india_gst_inhts
        cols.append(dfs["gts"].loc[(dfs["gts"]["Part Number"] == matnr), ["INHTS"]])
        # india_gst_stuec
        cols.append(
            dfs["marc"].loc[
                (dfs["marc"]["MATNR"] == matnr) & (dfs["marc"]["WERKS"] == plant),
                ["STEUC"],
            ]
        )
        # india_gst_taxm1
        cols.append(dfs["mlan"].loc[(dfs["mlan"]["MATNR"] == matnr), ["TAXM1"]])
        # china_energy_lbl
        cols.append(
            dfs["ausp"].loc[
                (dfs["ausp"]["OBJEK"] == matnr)
                & (dfs["ausp"]["ATINN"] == "STATUS_CHINA_ENERGY_LBL"),
                ["ATWRT"],
            ]
        )
        # cert
        cols.append("#N/a" if cert == "#N/A" else cert[7:])
        # cert name
        cols.append(cert)
        # cert status
        cols.append(
            dfs["ausp"].loc[
                (dfs["ausp"]["OBJEK"] == matnr) & (dfs["ausp"]["ATINN"] == cert),
                ["ATWRT"],
            ]
        )

        for idx, c in enumerate(cols):
            try:
                if isinstance(c, str):
                    part.append(c)
                elif isinstance(c, pd.DataFrame):
                    part.append(c.values[0][0])
                else:
                    part.append(c.values[0])
            except:
                part.append("#N/A")

        output = pd.DataFrame(parts, columns=columns_names)
        output.to_excel(
            os.path.join(os.environ["DIR_OUT"], "TEST_sap_load.xlsx"),
            index=False,
            # header=False,
        )

    return parts if len(parts) > 0 else []


def get_ext_cancelled():
    import os
    import pandas as pd

    sea_hub = kmats = pd.DataFrame()

    ext_cancel_file = os.path.join(os.environ["DIR_OUT"], "AP_CANCEL.txt")
    ext_cancel_df = pd.read_csv(ext_cancel_file, sep="\t")
    for i in range(7):
        ext_cancel_df[i] = ""
    print(list(ext_cancel_df.columns))
    sea_hub = ext_cancel_df.loc[ext_cancel_df["REQUESTER"].str.contains("sea hub")]
    kmats = ext_cancel_df.loc[ext_cancel_df["REQUESTER"].str.contains("KMAT")]
    return [sea_hub, kmats]
