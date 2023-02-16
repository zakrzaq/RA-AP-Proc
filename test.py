from helpers.helpers import output_msg
from helpers.log import load_log
from state.output import output
from test_mod import test_mod

try:
    log = load_log()
    output.add("LOG loaded")
except:
    output.add("LOG failed")


test_mod()

print(output.get_html())
