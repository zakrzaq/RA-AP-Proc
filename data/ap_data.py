def get_cert(sorg: int):
    match sorg:
        case 5003:
            return "STATUS_CCC"
        case 5008:
            return "STATUS_BIS"
        case 5010:
            return "STATUS_KC"
        case 5000 | 5012:
            return "STATUS_RCM"
        case 5016:
            return "STATUS_BSMI"
        case _:
            return "#N/A"


columns_names = [
    "date",
    "target_sorg",
    "target_plant",
    "requestor",
    "matnr",
    "service",
    "location",
    "req_catalogue",
    "req_material_type",
    "req_1k_dchain",
    "req_1k_cs",
    "req_reson",
    "req_comment",
    "req_legacy_no",
    "duplicate",
    "description",
    "catalog",
    "series",
    "mtart",
    "1k_dchain",
    "1k_cs",
    "1k_price",
    "4k_dchain",
    "4k_cs",
    "pgc",
    "target_sorg_price",
    "target_sorg_dchain",
    "target_sorg_DWERK",
    "target_sorg_cs",
    "target_sorg_pub",
    "target_plant_status",
    "target_plant_mrp_type",
    "dwerk_plant_status",
    "dwerk_plant_code",
    "mif_soerf_check",
    "sales_text",
    "india_gst_inhts",
    "india_gst_stuec",
    "india_gst_taxm1",
    "china_energy_lbl",
    "cert",
    "cert_name",
    "cert_status",
]
