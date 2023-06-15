def send_email(file=None):
    import win32com.client as win32
    from state.email import email as email_state
    from state.output import output
    import helpers.prompts as pr

    email = email_state.get()

    try:
        outlook = win32.GetActiveObject("Outlook.Application")
    except:
        outlook = win32.Dispatch("Outlook.Application")

    if outlook:
        mail = outlook.CreateItem(0)
        mail.To = email["to"]
        mail.cc = email["cc"]
        mail.Subject = email["subject"]
        mail.body = email["body"]
        if file != None:
            mail.Attachments.Add(file)
        mail.Send()
        outlook.Quit()

        email_state.reset()
        output.add(f"{pr.email}Email {email['subject']} sent")
    else:
        output.add(f"{pr.cncl}Failed to connect to Outlook")
