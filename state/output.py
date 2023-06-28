from markupsafe import Markup
from datetime import datetime
import os


class Output:
    messages = []
    html = ""

    def __init__(self):
        self.messages = []

    def add(self, input: str, css_class=["code-line"]):
        print(input)
        self.messages.append(input)
        class_list = ", ".join(css_class)
        self.html += f"<p class='{class_list}'>{input}</p>\n"

    def reset(self):
        self.messages = []
        self.html = ""

    def log(self):
        action_log_path = os.path.join(os.environ["DIR_LOG"], "action_log.txt")
        if not os.path.isfile(action_log_path):
            open(action_log_path, mode="a").close()
        with open(action_log_path, "r") as file:
            content = file.read()
        time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        all_messages = "\n".join(self.messages) if self.messages else ""
        to_log = time_str + "\n" + all_messages + "\n" + content
        with open(action_log_path, "w", encoding="utf-8") as file:
            file.write(to_log)

    def get(self):
        self.log()
        return self.messages

    def get_string(self):
        text = ""
        for mes in self.messages:
            text += mes + "\n"
        return text

    def get_html(self):
        return self.html

    def get_markup(self):
        self.log()
        return Markup(self.html)


output = Output()
