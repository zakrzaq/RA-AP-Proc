# AP MM EXTENSION BUSINESS ENGINE (APMMEBE)

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
\*\*file located in `C:\RA-Apps\AP-Proc`

```
RTD_USR='your_user_name'
RTD_PSW='your_password'
EDM_DRIVE='<your_end_drive_letter>:\Request Logs\Material Master Extension'
EDM_APMM='<your_end_drive_letter>:\Request Logs\APMM'
```

## USAGE

**IMPORTANT:** AP LOG file has to be closed on local machine to execute any scripts.

### Get current requests

AP Request form to be saved in `INPUTS` folder.

All new request will added to AP LOG

### Generate MIF / SOERF requests

This will genrate SQL Query file to your Desktop with name

### Update Material Statuses pre MM

> _to be written_

### Generate AM Price & PCE requests

Will output request files for Pricing & PCE requests. THose will be located in `OUTPUTS` folder.

### Update Material Statuses post MM Extension

> _to be written_

### Generate PM CCC, Localization & GTS Requests

Will output request files for GTS, Localization & CCC requests. THose will be located in `OUTPUTS` folder.

### DATA: Download SAP Data

All SAP data file to be saved in `OUTPUTS` folder.

> **Leave your computer for 5 minutes while it runs**

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

## TODO

- [x] Get SAP DATA
  - [x] fix data layout issues
  - [x] fix date issues
- [ ] Handle initial additions / CANCELLATIONS
- [x] Get current requests
- [x] Generate MIF/SOERF SQL Query
- [x] Update Material Statuses pre MM:
  - [x] fix query result for price and PCE
  - [ ] dates needing to be added to pce and price requests status updates
- [x] Generate AM Price & PCE requests
- [ ] Update Material Statuses post MM Extension
  - [ ] fix query result for price and PCE
- [x] Generate PM CCC, Localization & GTS Requests
- [x] CLI GUI with menu
- [ ] Error handling
  - [ ] try / except
  - [ ] error logging for CLI
  - [ ] error logging for API
- [x] SAP data import
  - [ ] LRF?
  - [x] AutoHotKey
- [ ] REST API using Flask
  - [ ] user interface
  - [ ] mechanics

## BUGFIXES

- [ ] check for log being open on every script
- [ ] MKVE.ahk SAP error
- [ ] BIS only on PCE status finder
- [ ] PCE finder to include Prod Cert Review

## MVP REQUIREMENTS:

- Business logic works correctly
- Training for some on operate CLI GUI in correct order // understanding the process
- external system access: SAP, Oracle RTD
-

## Notes

- Tyler Luoma for CR // is he Python?
-
