import os
from state.email import email
from helpers.emails import send_email
from data.email_notifications import ccc_email, inhts_email, local_email, test_email

readme = need_local_file = need_gts_file = need_pce_file = os.path.join(
    os.getcwd(), "README.md"
)

email.set(test_email)
send_email(readme)

email.set(ccc_email)
send_email(readme)


email.set(inhts_email)
send_email(readme)


email.set(localemail)
send_email(readme)
