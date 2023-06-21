from utils.workbook import load_log, save_log

sheet_list = [
    "Active Materials",
    "info",
    "mara",
    "marc",
    "mvke",
    "ausp",
    "mlan",
    "price",
    "gts",
    "sales_text",
    "mif",
    "soerf",
    "pce",
    "archived PCE",
]


class Log:
    def __init__(self):
        self.loaded = False
        self.workbook = None

    def __getitem__(self):
        return f"AP LOG file in SharePoint repository. Loaded: {self.loaded}"

    def save(self, *args, **kwargs):
        """Saves AP log file to Sharepoint"""
        print("kw", kwargs)
        save_log(self.workbook, *args, **kwargs) if self.loaded else None

    def insert_series(self, *args, **kwargs):
        pass

    def insert_df(self, *args, **kwargs):
        pass

    def get_last_row(self, *args, **kwargs):
        pass

    def extend_formulae(self, *args, **kwargs):
        pass

    def load(self):
        log = load_log()
        if log:
            self.loaded = True
            self.workbook = log
            self.ws_active = log["Active Materials"]
            self.ws_info = log["info"]
            self.ws_mara = log["mara"]
            self.ws_marc = log["marc"]
            self.ws_mvke = log["mvke"]
            self.ws_ausp = log["ausp"]
            self.ws_mlan = log["mlan"]
            self.ws_price = log["ZZ_MATPRC_HIST"]
            self.ws_gts = log["gts"]
            self.ws_text = log["sales text"]
            self.ws_mif = log["mif"]
            self.ws_soerf = log["soerf"]
            self.ws_pce = log["pce"]
            self.ws_pce_arch = log["archived PCE"]


log = Log()
