# AP MM EXTENSION PROCESS API

Developed for RA-INT to support extension of Material Master items with current demand to AP Region.

## REQUIREMENTS

`Windows` 7 and up

`Python` 3.9 and up

'make' command for terminal

> Google 'install make on windows' and follow the guide

## SETUP

Install Python on your local machine. Version `3.10` and up recommended.

Execute following commands from `Command Prompt`:

```bash
git clone <this repository key>
cd C:\RA-Apps
REN "RA-RA-AP-Proc" "AP-Proc"
cd AP-Proc
python setup.py
```

Edit corresponding lines in your `.env` using any text editor:
file located in `C:\RA-Apps\AP-Proc`

```bash
USER_NAME=Jakub Zakrzewski
API_URL=http://localhost:5000/
DIR_HOME=C:\Users\JZakrzewski
AP_LOG=${DIR_HOME}\Rockwell Automation, Inc\EDM - AP MM Service Request Process\AP MM Service Request Log.xlsm
# AP_LOG=${DIR_HOME}'\OneDrive - Rockwell Automation, Inc\Desktop\AP MM Service Request Log-test.xlsm'
ARC_LOG=${DIR_HOME}\Rockwell Automation, Inc\EDM - AP MM Service Request Process\Archived AP Material Master Service Requests.xlsx
AP_SHAREPOINT=${DIR_HOME}\Rockwell Automation, Inc\EDM - AP MM Service Request Process
AP_DB_DEV=${DIR_HOME}\Rockwell Automation, Inc\EDM - AP MM Service Request Process\apmm.db
DIR_DESKTOP=${DIR_HOME}\OneDrive - Rockwell Automation, Inc\Desktop
DIR_DOWNLOAD=${DIR_HOME}\Downloads
DIR_APP=C:\RA-Apps\AP-Proc
DIR_IN=${DIR_APP}\INPUTS
DIR_OUT=${DIR_APP}\OUTPUTS
DIR_LOG=${DIR_APP}\logs
EDM_DRIVE=Z:\Request Logs\Material Master Extension
EDM_APMM=Z:\Request Logs\APMM

```

Edit corresponding lines in your `.rtd_config.py` using any text editor:
file located in `C:\RA-Apps\AP-Proc\configs`

```python
RTD_USR='your_user_name'
RTD_PSW='your_password'
RTD_STR='rtd db connection string'
```

Edit corresponding lines in your `.sap.py` using any text editor:
file located in `C:\RA-Apps\AP-Proc\configs`

```python
username = "jzakrzewski"
password = "AlexEllaJudy2023!"
path = "C:\Program Files (x86)\SAP\FrontEnd\SapGui\saplgpad.exe"
```

## USAGE

Execute via `make run-cli` for CLI Interface

Execute via `make run-server` for web interface accessible on [here](http://localhost:5000)

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

Will bring SAP data from files fetched in previous step to AP LOG.

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

- [ ] am_status to handle PROD CERT by review date
- [ ] first run of sqvi, gts hang up on save to Excel
- [ ] [Rafael] improve excel DATE FORMATS
- [x] spelling elapsed_time & fix Timer class to use in scripts - 2023-06-22 
- [x] mif_soerf.py today_dmy UNBOUND - 2023-06-22
- [x] update setup and readme - 2023-06-21
- [x] fix env and file location not loading - 2023-06-21
- [x] refactor sap data to class based system - 2023-06-21
- [x] refactor log data to class based system - 2023-06-21
- [x] refactor all code for readability - 2023-06-21
- [x] status messages on SAP data script - 2023-06-21
- [x] archive PCE requests file name issue - 2023-06-21
- [x] mif / soerf ext data populate - wrong last row / crash - 2023-06-21
- [x] fix win32 CoInitlized issus with Excel / Outlook - 2023-06-21

## NEW FEATURES REQUESTS

- [ ] New business rule for certain parts in 5008 for Ryne identified by Sales Text

## TODO 1.5

- [ ] integrate proper front and with conditional style like AP Log
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
- [x] email notification for PCE, CC, PRICE, INHTS, LOCAL requests

## TODO 0.5

- [x] Get SAP DATA
  - [x] fix data layout issues
  - [x] fix date issues
- [ ] Handle initial additions / CANCELLATIONS
  - [ ] amend existing request form
  - [ ] new request form and data source
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
  - [x] AutoHotKey
  - [ ] more repliable solution needed
- [x] REST API using Flask
  - [x] user interface
  - [x] mechanics

## MVP REQUIREMENTS:

- Business logic works correctly
- Training for some on operate CLI GUI in correct order // understanding the process
- external system access: SAP, Oracle RTD

## Notes
