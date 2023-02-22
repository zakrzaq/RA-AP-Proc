class Email:
    def __init__(self):
        self.to = ""
        self.cc = ""
        self.subject = ""
        self.body = ""

    def __repr__(self) -> str:
        return f"Subject: {self.subject} to: {self.to}"

    def reset(self):
        self.to = None
        self.cc = None
        self.subject = None
        self.body = None

    def set(self, dict):
        self.to = dict["to"]
        self.cc = dict["cc"]
        self.subject = dict["subject"]
        self.body = dict["body"]

    def get(self):
        return {
            "to": self.to,
            "cc": self.cc,
            "subject": self.subject,
            "body": self.body,
        }


email = Email()
