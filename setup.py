import platform
import os


sys_type = platform.system().lower()


if sys_type == "windows":
    os.system("python -m venv venv")
    os.system("clear")
    os.system(".\venv\Scripts\activate")
    os.system("clear")
    os.system("pip install -r requirements.txt")
    os.system("clear")
    os.system("echo .\venv\Scripts\activate >> ap_cli.bat")
    os.system("echo python ap_proc.py >> ap_cli.bat")
    os.system("clear")
    os.system("echo .\venv\Scripts\activate >> ap_server.bat")
    os.system("echo flask --debug run --host=0.0.0.0 >> ap_server.bat")
else:
    os.system("python -m venv .env")
    os.system("clear")
    os.system("source ./.env/bin/activate")
    os.system("clear")
    os.system("pip install -r requirements.txt")
    os.system("clear")
    ap_proc = "#!/bin/bash\nsource env/bin/activate\npython ap_proc.py"
    f = open("ap_cli.sh", "w")
    f.write(ap_proc)
    f.close()
    ap_serv = "#!/bin/bash\nsource env/bin/activate\nflask --debug run --host=0.0.0.0"
    f = open("ap_server.sh", "w")
    f.write(ap_serv)
    f.close()
    os.system("chmod +x ./ap_server.sh")
    os.system("chmod +x ./ap_cli.sh")


# FIND DESKTOP FOLDER
# username = os.getlogin()
# usersdir = r'C:\Users'
# homedir = os.path.join(usersdir, username)
# # print(homedir)
# for root, dirs, files in os.walk(homedir):
#     for folder in dirs:
#       # path = os.path.join(homedir, dirs, folder)
#         if (folder == "Desktop"):
#             path = os.path.join(root, folder)
#             if 'OneDrive - Rockwell Automation, Inc' in path:
#                 # print(path)
#                 ["HOME_DIR"] = path
#                 dotenv.set_key(dotenv_file, "HOME_DIR", os.environ["HOME_DIR"])

# appdir = os.path.join(path, dev_folder)
# os.environ["APP_DIR"] = appdir
# dotenv.set_key(dotenv_file, "APP_DIR", os.environ["APP_DIR"])

# download_dir = os.path.join(homedir, downloads_folder)
# os.environ["DWN_DIR"] = download_dir
# dotenv.set_key(dotenv_file, "DWN_DIR", os.environ["DWN_DIR"])

# tmp_out_dir = os.path.join(devdir, tmp_output_folder)
# os.environ["TMP_OUT_DIR"] = tmp_out_dir
# dotenv.set_key(dotenv_file, "TMP_OUT_DIR",
#                os.environ["TMP_OUT_DIR"])

# for root, dirs, files in os.walk(homedir):
#     for folder in dirs:
#       # path = os.path.join(homedir, dirs, folder)
#         if (folder == "EDM - AP MM Service Request Process"):
#             sp_path = os.path.join(root, folder)
#             print(sp_path)
#             os.environ["AP_SHAREPOINT"] = sp_path
#             dotenv.set_key(dotenv_file, "AP_SHAREPOINT",
#                            os.environ["AP_SHAREPOINT"])

#             log_name = 'AP MM Service Request Log.xlsm'
#             lg_path = os.path.join(sp_path, log_name)
#             os.environ["AP_LOG"] = lg_path
#             dotenv.set_key(dotenv_file, "AP_LOG",
#                            os.environ["AP_LOG"])


# # print(os.environ["HOME_DIR"])  # outputs "value"
# # os.environ["key"] = "newvalue" # create kay, assign value
# # print(os.environ['key'])  # outputs new key

# # Write changes to .env file.
# # dotenv.set_key(dotenv_file, "key", os.environ["key"])
