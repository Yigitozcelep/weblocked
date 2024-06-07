import keyring
from datetime import datetime
import subprocess
import pexpect


keyring_date_data_service            = "asdlafAsd023912039as09Dasdo0zx9c001om"
keyring_date_data_username           = "sadklasdasdoak102e12e021kem0mzMADas1m"

keyring_terminal_password_service    = "asdmozxcpapasdop12lm3001320zxcad0ASdx"
keyring_terminal_password_username   = "ASDmocxmzoc0asd012easpadsmaspxizxckma"

keyring_phone_password_service       = "asdadasdasdasm0x901230xAm1asd0123xmapoqk"
keyring_phone_password_username      = "asdzmxmamMMMasdzxc091230asdxzcmappqmzAmt"

keyring_phone_data_service           = "asdmxczmmMASMDAMSMDzoads12309123mzczasd01Xasd"
keyring_phone_data_username          = "amsdasmdomdOMADSMASDMAom12301aASDOIXZCmpaoqma"

current_service_data = "3" * 1000
current_password = "01MAx=asd,!0MxzASDomzxcAP3#[a=1230X(masdp>Sdm23-"


def run_command(query):
    command = "sudo " + " ".join(query.split(" ")[1:])
    child = pexpect.spawn(command)
    child.expect("Password")

    child.sendline('"+dd&!A:>l%?B+p;9/M5')
    child.interact()

    


def open_command(query):
    pass

def add_forbidden(query):
    pass

def get_count_phone():
    pass

def get_forbiddens():
    pass

def get_count():
    pass


def get_phone_password():
    pass

print("+----------------------------------- Commands -----------------------------------+")
print("| run             \\\ run commands in sudo example run rm -rf xx = sudo rm -rf xx |")
print("| get_count       \\\ get count of the urgent open for this month                 |")
print("| open            \\\ open the forbidden aplication example open all              |")
print("| get_forbiddens  \\\ get names of forbidden applications                         |")
print("| add_forbidden   \\\ example usage add_forbidden 127.0.0.1 www.youtube.com       |")
print("| get_count_phone \\\ get count of urgen open phone for this month                |")
print("| phone_password  \\\ show the phone password                                     |")
print("| quit(q)         \\\ quit from application                                       |")

query = input()
while query != "q" or query != "quit":
    if             "run"  in query: run_command(query)
    elif          " open" in query: open_command(query)
    elif "add_forbidden"  in query: add_forbidden(query)
    elif "query" == "get_count_phone" : get_count_phone()
    elif "query" == "get_forbiddens"  : get_forbiddens()
    elif "query" == "get_count"       : get_count()
    elif "query" == "phone_password"  : get_phone_password()
    query = input()

print("aplication is closed")










