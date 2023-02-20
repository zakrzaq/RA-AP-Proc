# AP MM EXTENSION PROCESS API

Developed for RA-INT to support extension of Material Master items with current demand to AP Region.

## REQUIREMENTS

`Windows` 7 and up

`Python` 3.10 and up

## SETUP

Install Python on your local machine. Version `3.10` and up recommended.

Execute following commands from `Command Prompt`:

```
git clone <this repository key>
cd C:\RA-Apps
REN "RA-RA-AP-Proc" "AP-Proc"
cd AP-Proc
python setup.py
```

Edit corresponding lines in your `.env` using any text editor:
file located in `C:\RA-Apps\AP-Proc`

```
EDM_DRIVE='<your_end_drive_letter>:\Request Logs\Material Master Extension'
EDM_APMM='<your_end_drive_letter>:\Request Logs\APMM'
```

Edit corresponding lines in your `.rtd_config.py` using any text editor:
file located in `C:\RA-Apps\AP-Proc`

```
RTD_USR='your_user_name'
RTD_PSW='your_password'
RTD_STR='rtd db connection string'
```

## USAGE

Execute via `ap_proc.bat` for CLI Interface

Execute via `ap_serv.bat` for web interface accessible on [here](http://localhost:5000)

**IMPORTANT:** AP LOG file has to be closed on local machine to execute any scripts.

### Get current requests

AP Request form to be saved in `INPUTS` folder.

All new request will added to AP LOG

### Generate MIF / SOERF requests

This will process SQL query and:

- generate MIF & SOURF request files in `OUTPUTS` directory
- add new mif, soerf data to AP LOG
- generate file `AP_CANCEL` in `OUTPUTS` directory with additional extension and exceptions - **to be added to LOG manually**

### Update Material Statuses pre MM

> _to be written_

### Generate AM Price & PCE requests

Will output request files for Pricing & PCE requests. Those will be located in `OUTPUTS` folder.

### Reconcile PCE Requests / Update ORG SOURCE

> _to be written_

### Update Material Statuses post MM Extension

> _to be written_

### Generate PM CCC, Localization & GTS Requests

Will output request files for GTS, Localization & CCC requests. THose will be located in `OUTPUTS` folder.

### DATA: Download SAP Data

All SAP data file to be saved in `OUTPUTS` folder.

> **Leave your computer for ~5 minutes while it runs**

REQUIRED FILES:

```
mara.xlsx
marc.xlsx
mvke.xlsx
ausp.xlsx
mlan.xlsx
price.xlsx
gts.xlsx
sales_text.xlsx
```

### DATA: Bring SAP Data

Will bring SAP data to AP LOG.

### UTILITY: Clean working folder & archive request files

To be run at the end of a day or after **am** and **pm** run.

Archive work files and uploads request files to EDM Drive.

### UTILITY: Check for MIF/SOERF submitted

Will produce out put showing for both MIF/SOERF to AP MM Extension Process:

- if there is a file submitted for today
- quick list of MIF/SOERF included in the file
- count of current file submissions for MIF/SOERF in AP MM Extension Process

### UTILITY: Check for daily report uploaded to Sharepoint Repository

Will produce out indicating if report file for current day is present in Sharepoint Repository.

### UTILITY: Open SAP Instance

Open SAP instance using browser. No to touch mouse / keyboard while it runs

### Update program

Will run git command to update to latest changes available on repository.

### Close program

It says it on the tin.

## BUGFIXES

- [x] check for log being open on every script
- [ ] archive PCE requests file name issue
- [ ] am_status to handle PROD CERT by review date
- [x] MKVE|MARC.ahk SAP error/crash on large data loads
  - [x] AHK reliability SE16
  - [ ] AHK reliability rest
- [ ] get SAP data lower/upper case file name issue
- [ ] improve excel DATE FORMATS
- [] mif / sorf data bring incorrect date
- [x] BIS only on PCE status finder
- [x] PCE finder to include Prod Cert Review
- [x] Flask: Check daily report server error
- [x] Flask: clean server error

## TODO 1.5

- [ ] integrate proper front and with conditial style like AP Log
- [ ] hosted db

## TODO 1.0

- [ ] SQLITE DB
  - [x] sharepoint or ~~local~~?
  - [x] data model to reflect AP LOG
  - [ ] AP LOG VIEW - **WIP**
  - [ ] search query and parameters
  - [ ] fetch new request from data source
  - [ ] archive new requests to data source
  - [ ] find way to use templates and return data as same time in FLASK
  - [ ] requests to db
- [ ] BE able to run on milwaukee machine / ip address for vpn network

## TODO 0.5

- [x] Get SAP DATA
  - [x] fix data layout issues
  - [x] fix date issues
- [ ] Handle initial additions / CANCELLATIONS
  - [ ] amend existing request form
  - [ ] new request form and dat source
- [x] Get current requests
- [x] Generate MIF/SOERF SQL Query
  - [x] using CLI Oracle CS for query running and data
- [x] Update Material Statuses pre MM:
  - [x] fix query result for price and PCE
  - [x] dates needing to be added to pce and price requests status updates
- [x] Generate AM Price & PCE requests
- [x] Update Material Statuses post MM Extension
  - [x] fix query result for price and PCE
- [x] Reconcile PCE & Original Source
  - [x] org_source - list of material from df
  - [x] org_source - ahk query
  - [x] reconcile PCE - update log
  - [x] reconcile PCE - update load file
  - [x] reconcile PCE - update ahk script
- [x] Generate PM CCC, Localization & GTS Requests
- [x] CLI GUI with menu
- [x] Error handling
  - [x] try / except v1
  - [x] try / except v2
  - [x] error logging for CLI
  - [x] error logging for API
- [x] SAP data import
  - [ ] LRF? current 8 scripts / on LFR will 10 + 2
  - [x] AutoHotKey
- [x] REST API using Flask
  - [x] user interface
  - [x] mechanics

## MVP REQUIREMENTS:

- Business logic works correctly
- Training for some on operate CLI GUI in correct order // understanding the process
- external system access: SAP, Oracle RTD

## Notes

> Tyler Luoma for CR // is he Python?
