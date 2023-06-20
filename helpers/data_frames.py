import os
import pandas as pd

from helpers.helpers import use_dotenv
import helpers.prompts as pr
from state.output import output

use_dotenv()


def df_to_list(df: pd.DataFrame) -> list:
    """Converts DF to python list of lists.

    Args:
    df: DataFrame

    Returns:
    []
    """
    out = []
    for i, r in df.iterrows():
        row = []
        for n in r.values:
            row.append(n)
        out.append(row)
    return out


def get_active(sheet_name="Active Materials"):
    try:
        df = pd.read_excel(os.environ["AP_LOG"], sheet_name=sheet_name, dtype=str)
        output.add(f"{pr.ok}LOG data obtained")
        return df
    except:
        output.add(f"{pr.cncl}LOG data failed to download")
        return pd.DataFrame()


def get_selected_active():
    try:
        active = get_active()
        return active[
            [
                "Date Added",
                "target sorg",
                "target plant",
                "email prefix\n(from request form)",
                "SAP MATNR\n(from request form)",
                "Service Requested\n(from request form)",
                "Location\n(from request form)",
                "Catalog",
                "Ser",
                "MTART/GenItemCat",
                " sorg1k dchain",
                " sorg1k cs",
                "sorg1k price",
                " sorg4k dchain",
                " sorg4k cs",
                "PGC",
                "target sorg price",
                "target sorg dchain",
                "target sorg DWERK",
                "target sorg cs",
                "target sorg pub",
                "target plant status",
                "target plant mrp type",
                "DWERK Plant Status",
                "DWERK Plant Code",
                "mif/soerf check",
                "Sales Text",
                "INDIA GST\nINHTS",
                "INDIA GST\nmarc.stuec",
                "INDIA GST taxm1",
                "STATUS_CHINA_ENERGY_LBL",
                "Regulatory Cert\n(Z62 Class)",
                "Regulatory Cert\n(Z62 Characteristic)",
                "Z62 characteristic\n(assigned in SAP)",
                "PCE Assessment\n(received)",
                "Date of PCE review",
                "MIF Submitted",
                "SOERF Submitted",
                "pricing request",
                "PCE cert rev req'd",
                "status",
                "sort order",
            ]
        ]
    except:
        output.add(f"{pr.cncl}Failed getting Selected Active View")
        return pd.DataFrame()


def get_active_requests():
    df = get_active()
    df["Date Added"] = pd.to_datetime(df["Date Added"], errors="coerce").dt.strftime(
        "%d/%m/%Y"
    )
    df = df.fillna("")
    df = df.iloc[:, :14]
    out = df_to_list(df)
    return out if len(out) > 0 else []


def get_archive(sheet_name="archive starting 3-15-2014"):
    try:
        df = pd.read_excel(os.environ["ARC_LOG"], sheet_name=sheet_name, dtype=str)
        output.add(f"{pr.ok}ARCHIVE data obtained")
        return df
    except:
        output.add(f"{pr.cncl}ARCHIVE data failed to download")
        return pd.DataFrame()


def get_selected_archive():
    try:
        active = get_archive()
        return active[
            [
                "Date Added",
                "target sorg",
                "target plant",
                "email prefix\n(from request form)",
                "SAP MATNR\n(from request form)",
                "Service Requested\n(from request form)",
                "Location\n(from request form)",
                "Catalog",
                "Ser",
                "MTART/GenItemCat",
                " sorg1k dchain",
                " sorg1k cs",
                "sorg1k price",
                " sorg4k dchain",
                " sorg4k cs",
                "PGC",
                "target sorg price",
                "target sorg dchain",
                "target sorg DWERK",
                "target sorg cs",
                "target sorg pub",
                "target plant status",
                "target plant mrp type",
                "DWERK Plant Status",
                "DWERK Plant Code",
                "mif/soerf check",
                "Sales Text",
                "Regulatory Cert\n(Z62 Class)",
                "Regulatory Cert\n(Z62 Characteristic)",
                "Z62 characteristic\n(assigned in SAP)",
                "PCE Assessment\n(received)",
                "Date of PCE review",
                "MIF Submitted",
                "SOERF Submitted",
                "pricing request",
                "PCE cert rev req'd",
                "status",
                "sort order",
            ]
        ]
    except:
        output.add(f"{pr.cncl}Failed getting Selected Archive View")
        return pd.DataFrame()


def handle_eod_report(file):
    report = pd.read_excel(file)
    print(report.head())
    total = report.shape[0]
    completed = report.loc[
        report["status"].str.contains("complete", case=False) == True
    ].shape[0]
    cancelled = report.loc[
        report["status"].str.contains("cancel", case=False) == True
    ].shape[0]
    on_hold = report.loc[
        report["status"].str.contains("on hold", case=False) == True
    ].shape[0]
    in_progress = total - completed - cancelled - on_hold

    output = {
        "total": total,
        "completed": completed,
        "cancelled": cancelled,
        "on_hold": on_hold,
        "in_progress": in_progress,
    }

    return output


def get_single_sap(table: str) -> pd.DataFrame:
    """Loads SAP table Excel data from file in INPUTS dir.

    Args:
    table (str): <mara | marc | mvke | ausp | mlan | price | gts | sales_text>

    Returns:
    Pandas DataFrame | None"""

    table = table.lower()
    filename = table + ".xls" if table == "sales_text" else table + ".xlsx"
    if table == "sales_text":
        df = pd.read_csv(
            os.path.join(os.environ["DIR_IN"], filename), sep="\t", encoding="utf-16"
        )
    else:
        df = pd.read_excel(os.path.join(os.environ["DIR_IN"], filename))
    return df if not df.empty else pd.DataFrame()
