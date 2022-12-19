def await_char(param, func="", msg=""):
    import keyboard
    if msg == "":
        msg_out = 'Press {} to continue'.format(param.upper())
    else:
        msg_out = msg
    print(msg_out)
    while True:
        if keyboard.is_pressed("c"):
            break
        if keyboard.is_pressed("C"):
            break
        if keyboard.is_pressed(param):
            if func:
                func()
            break
