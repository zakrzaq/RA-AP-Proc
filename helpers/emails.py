def send_email(file):
    import win32com.client as win32
    from state.email import email as email_state
    from state.output import output
    import helpers.prompts as pr

    email = email_state.get()

    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)
    mail.To = email["to"]
    mail.cc = email["cc"]
    mail.Subject = email["subject"]
    mail.body = email["body"]
    mail.Attachments.Add(file)
    mail.Send()

    email_state.reset()
    output.add(f"{pr.email}Email {email['subject']} sent")
