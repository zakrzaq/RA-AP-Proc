from markupsafe import Markup


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

    def get(self):
        return self.messages

    def get_string(self):
        text = ""
        for mes in self.messages:
            text += mes + "\n"
        return text

    def get_html(self):
        return self.html

    def get_markup(self):
        return Markup(self.html)


output = Output()
