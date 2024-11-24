import os
from datetime import datetime

def eprint(message: str):
    _eprint(message)


def dprint(message: str):
    _dprint(message)


def read_file(file_path: str) -> str:
    return _read_file(file_path)


def check_json_error(data: dict[str], key: str) -> str:
    return _check_json_error(data, key)


def load_json(data: str) -> dict[str]:
    return _load_json(data)


current_user = os.environ.get("USER").capitalize()
if current_user == None:
    current_user = ""

config = data_input["config_path"]
customer_name = data_input["customer_name"]
dprint(config)

if config == None:
    eprint("config file is empty")
    exit(1)

if customer_name == None:
    eprint("customer name is empty")
    exit(1)

buffer = read_file(config)
data = load_json(buffer)
customers = check_json_error(data, "customers")

if customers == None:
    eprint("no data was found in the customer config file")
    exit(1)

eml_to = []
eml_cc = []
c_name = ""
c_prefix = ""
subject = ""

for i in customers:
    name = check_json_error(i, "name")
    prefix = check_json_error(i, "prefix")

    if name != None and name == customer_name:
        c_name = name
        c_prefix = prefix
        eml_to = check_json_error(i, "to")
        eml_cc = check_json_error(i, "cc")
        break

    elif prefix != None and prefix == customer_name:
        c_name = name
        c_prefix = prefix
        eml_to = check_json_error(i, "to")
        eml_cc = check_json_error(i, "cc")
        break

subject = f"Suspicious activity detected in the {c_prefix} network"
eml_to_str = ""
eml_cc_str = ""

if eml_to != None:
    for i in eml_to:
        eml_to_str += i + "; "

if eml_cc != None:
    for i in eml_cc:
        eml_cc_str += i + "; "

now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S %p").replace(",", " at")
data_output["my_company"] = "ByteBox"
data_output["alert_name"] = "Suspicious activity detected"
data_output["current_time"] = now
data_output["current_loggedin_user"] = current_user
data_output["to"] = eml_to_str
data_output["cc"] = eml_cc_str
data_output["prefix"] = c_prefix
data_output["customer_name"] = c_name
data_output["subject"] = subject