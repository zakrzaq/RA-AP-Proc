import os
import dotenv

# FIND AND FOLAD DOT ENV
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


os.system("python -m pip install --upgrade pip")
os.system("pip install virtualenv")
os.system("python -m venv env")
os.system("env/Scripts/activate.bat")
os.system('env/Scripts/Activate.ps1')
os.system(
    "pip install -r requirements.txt")
# os.system("pip list")
os.system("echo call env/Scripts/activate.bat >> ap_proc.bat")
os.system("echo call env/Scripts/Activate.ps1 >> ap_proc.bat")
os.system("echo python ap_proc.py >> ap_proc.bat")
os.system("echo flask run >> ap_serv.bat")


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
