def await_char(char, msg="", func="", param=""):
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
