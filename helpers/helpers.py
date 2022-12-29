import os
import dotenv
import warnings
import logging


def await_char(char="y", msg="", func="", param=""):
    import keyboard
    if msg == "":
        msg_out = f'Press {char.upper()} to continue'
    else:
        msg_out = msg
    print(msg_out)
    while True:
        if keyboard.is_pressed("c"):
            break
        if keyboard.is_pressed("C"):
            break
        if keyboard.is_pressed(char):
            if func != "":
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
    logging.basicConfig(filename=os.path.join(
        "logs", "log.txt"), level=logging.DEBUG)
