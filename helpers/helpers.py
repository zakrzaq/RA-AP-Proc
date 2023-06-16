import os
import dotenv
import warnings
import logging
import platform
import pythoncom

from state.output import output


def await_char(char="y", msg="Press Y to continue", func=None, param=""):
    import keyboard

    if msg == "":
        msg_out = f"Press {char.upper()} to continue"
    else:
        msg_out = msg
    print(msg_out)
    while True:
        if keyboard.is_pressed("c"):
            break
        if keyboard.is_pressed("C"):
            break
        if keyboard.is_pressed(char):
            if func:
                if param != "":
                    func(param)
                else:
                    func()
            break


def use_dotenv():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)


def ignore_warnings():
    warnings.filterwarnings("ignore")


def use_logger():
    logging.basicConfig(filename=os.path.join("logs", "log.txt"), level=logging.DEBUG)


def end_script(server):
    if not server:
        await_char()
    return output.get_markup()


def format_pce_price_dates(x: str) -> str:
    # print(x)
    if str(x) == "comp":
        return str(x)
    elif str(x) == "nan":
        return ""
    elif len(str(x)) > 10:
        if "-" in str(x):
            x = str(x).replace("-", "/")
        return str(x)[5:-9]
    elif len(str(x)) == 10:
        if "-" in str(x):
            x = str(x).replace("-", "/")
        return str(x)[5:]
    else:
        return str(x)


def format_request_date(x: str) -> str:
    if "-" in str(x):
        x = str(x).replace("-", "/")
    return str(x)[:-9]


def clear():
    if platform.system() == "Windows":
        return os.system("cls")
    else:
        return os.system("clear")


def coinit():
    pythoncom.CoInitialize()
