import os
import dotenv
import warnings
import logging
import platform
import pythoncom

import utils.prompts as pr

from state.output import output


def await_char(
    char="y",
    message=None,
    func=None,
    *args,
):
    import keyboard

    prompt = f"{pr.prmt}Press {char.upper()} to continue" + ". Press C to cancel"

    if message == None:
        msg_out = prompt
    else:
        msg_out = message + "\n" + prompt
    print(msg_out)
    while True:
        if keyboard.is_pressed("c"):
            break
        if keyboard.is_pressed("C"):
            break
        if keyboard.is_pressed(char):
            if func:
                func(*args)
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


def use_coinit():
    pythoncom.CoInitialize()


def check_file(file_path: str, create=False) -> bool:
    if os.path.isfile(file_path):
        return True
    else:
        if create:
            open(file_path, mode="a").close()
            return True
        else:
            return False


def check_dir(dir_path: str, create=False) -> bool:
    if os.path.isdir(dir_path):
        return True
    else:
        if create:
            os.mkdir(dir_path)
            return True
        else:
            return False


def get_dictionary_value(lst, key, value, return_value):
    for dictionary in lst:
        if dictionary.get(key) == value:
            return dictionary[return_value]
    return ""
