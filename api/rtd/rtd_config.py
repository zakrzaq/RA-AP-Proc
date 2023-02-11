import os
from helpers.helpers import use_dotenv

use_dotenv()

username = "jzakrze"
password = "raint2022"
RTD = "(description = (address_list = (address = (protocol = tcp)(host = mkeudb3110.mke.ra.rockwell.com)(port = 1534))) (connect_data =(service_name = rtd.mke.ra.rockwell.com)(instance_name = JAMESON)))"

# username = os.environ["RTD_USR"]
# password = os.environ["RTD_PSW"]
# RTD = os.environ["RTD_STR"]
