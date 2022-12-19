def await_char(param, func=""):
    import keyboard
    print('Press {} to continue'.format(param.upper()))
    while True:
        if keyboard.is_pressed(param):
            if func:
                func()
            break
