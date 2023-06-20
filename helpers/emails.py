def send_email(file=None):
    import win32com.client as win32

    from state.email import email as email_state
    from state.output import output
    import helpers.prompts as pr
    from helpers.helpers import use_coinit

    use_coinit()

    email = email_state.get()

    outlook = win32.Dispatch("Outlook.application")

    if outlook:
        mail = outlook.CreateItem(0)
        mail.To = email["to"]
        mail.cc = email["cc"]
        mail.Subject = email["subject"]
        mail.body = email["body"]
        if file != None:
            mail.Attachments.Add(file)
        mail.Send()

        email_state.reset()
        output.add(f"{pr.email}Email {email['subject']} sent")
    else:
        output.add(f"{pr.cncl}Failed to connect to Outlook")
