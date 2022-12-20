import dotenv
import warnings


def await_char(char="y", msg="", func="", param=""):
    import keyboard
    if msg == "":
        msg_out = 'Press {} to continue'.format(char.upper())
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
