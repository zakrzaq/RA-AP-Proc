# AP MM EXTENSION BUSINESS ENGINE (APMMEBE)

Written for RA-INT to support extension of Material Master items with current demand to AP Region.

## SETUP

run `python ./IN-DEV/setup_env.py` to generate system paths fro app and install dependencies. NOTE - python has to installed on the system beforehand.

edit `.env` key `EDM_DRIVE` to your path
e.g. `EDM_DRIVE='Z:\\Request Logs\\Material Master Extension\\'`

## REQUIREMENTS

Python 3.10
Pandas `pip install pandas`
OpenPyXl

## TODO

- [] fix data issues on 0_SAP_DATA. date issues
- [] MIF_SOERF: dates needing to be added to pce and price requests
- [] front end menu
- [] reuquest validate service requested

## MVP:

-
