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
