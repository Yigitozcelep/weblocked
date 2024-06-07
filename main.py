import keyring
import datetime
import subprocess
import pexpect


initial_date = datetime.datetime.strptime("2024-06-07 00:00:00", "%Y-%m-%d %H:%M:%S")

keyring_date_data_service             = "asdlafAsd023912039as09Dasdo0zx9c001om"
keyring_date_data_username            = "sadklasdasdoak102e12e021kem0mzMADas1m"

keyring_terminal_password_service     = "asdmozxcpapasdop12lm3001320zxcad0ASdx"
keyring_terminal_password_username    = "ASDmocxmzoc0asd012easpadsmaspxizxckma"

keyring_phone_password_service        = "asdadasdasdasm0x901230xAm1asd0123xmapoqk"
keyring_phone_password_username       = "asdzmxmamMMMasdzxc091230asdxzcmappqmzAmt"

keyring_phone_data_service            = "asdmxczmmMASMDAMSMDzoads12309123mzczasd01Xasd"
keyring_phone_data_username           = "amsdasmdomdOMADSMASDMAom12301aASDOIXZCmpaoqma"

keyring_app_name_and_address_service  = "asdkadoasmMasodasd9123asdmzxcoasd101239Xmasd1"
keyring_app_name_and_address_username = "asdkAAsmMasoAAdasd9123asdmzxcoasMa9sd1AoasdAX"

keyring_accessible_days_service       = "asmdMMAsdmaxnzNNNasdaxcASDamp1239A912mAxoasdxp"
keyring_accessible_days_username      = "DAsdmammaODODpadahasdMAsdosadmPqwe20123mAsdo12"

current_service_data = "3" * 1000
current_password = "01MAx=asd,!0MxzASDomzxcAP3#[a=1230X(masdp>Sdm23-"
phone_password   = "phone_password1"



def calc_month_dif(d1, d2):
    return abs(12 * (d1.year - d2.year) + (d1.month - d2.month))

def get_initial_today_month_dif():
    return int(calc_month_dif(datetime.datetime.today(), initial_date))


def run_command(query):
    if "etc/hosts" in query:
        print("weblocked progrem error etc/hosts can not be in query")
        return
    
    command = "sudo " + " ".join(query.split(" ")[1:])
    child = pexpect.spawn(command)
    child.expect("Password")
    child.sendline('"+dd&!A:>l%?B+p;9/M5')
    child.interact()


def open_command(query):
    count = get_count()
    if count <= 0:
        print("your count is 0 you can not open forbidden application")
        return
    
    decrement_count()
    

def add_forbidden(query):
    pass

def get_count_phone():
    date_data = keyring.get_password(keyring_phone_data_service, keyring_phone_data_username)
    return int(date_data[get_initial_today_month_dif()])


def get_forbiddens():
    pass

def get_count():
    date_data = keyring.get_password(keyring_date_data_service, keyring_date_data_username)
    return int(date_data[calc_month_dif(datetime.datetime.today(), initial_date)])

def decrement_count():
    date_data = keyring.get_password(keyring_date_data_service, keyring_date_data_username)
    month_dif = get_initial_today_month_dif()
    updated_val = int(date_data[month_dif]) - 1
    date_data = date_data[:month_dif] + str(updated_val) + date_data[month_dif + 1:]
    keyring.set_password(keyring_date_data_service, keyring_date_data_username, date_data)


def get_free_opens():
    return keyring.get_password(keyring_accessible_days_service, keyring_accessible_days_username)
    

def print_phone_password():
    count = get_count_phone()
    if count > 0: print("password: ", keyring.get_password(keyring_phone_password_service, keyring_phone_password_username))
    else: print("your phone count is 0 you can not look your password")

def set_new_open(query):
    _, day1, day2 = query.split(" ")
    def check(d):
        if len(d) != 7: print(f"wrong input format {d} your input length should be 7")
        elif d[1] != ":" or d[4] != "-": print(f"wrong input format {d} input should contain ':' and '-' for example 5:12-40")
        elif not d[0].isnumeric() or not d[2].isnumeric() or not d[3].isnumeric() or not d[5].isnumeric() or not d[6].isnumeric(): print(f"wrong input format {d} day format should be numeric")
        elif int(d[2] + d[3]) > 24 or int(d[5] + d[6]) > 60: print(f"wrong input format {d} hour should not be more than 24 and minute should not be more than 60")
        else: return True
        return False
    
    if not check(day1) or not check(day2): return
    keyring.set_password(keyring_accessible_days_service, keyring_accessible_days_username, day1 + "|" + day2)
    print("new date is successfully updated")


def help_command(query):
    pass

print("+------------------------------------ Commands ------------------------------------+")
print("| run             \\\ run commands in sudo example run rm -rf xx = sudo rm -rf xx   |")
print("| get_count       \\\ get count of the urgent open for this month                   |")
print("| open_forbiddens \\\ open the forbidden aplication example open all                |")
print("| get_forbiddens  \\\ get names of forbidden applications                           |")
print("| get_free_opens  \\\ get days hours of free open                                   |")
print("| set_new_open    \\\ this set new open date example set_new_open 0:12-40 6:10-30   |")
print("| add_forbidden   \\\ example usage add_forbidden youtube|127.0.0.1 www.youtube.com |")
print("| get_count_phone \\\ get count of urgen open phone for this month                  |")
print("| phone_password  \\\ show the phone password                                       |")
print("| help_command    \\\ examples help run or help open it gives detailed explanation  |")
print("| quit(q)         \\\ quit from application                                         |")


query = input()
while query != "q" and query != "quit":
    if             "run"   in query: run_command(query)
    elif   "set_new_open"  in query: set_new_open(query)
    elif "open_forbiddens" in query: open_command(query)
    elif "add_forbidden"   in query: add_forbidden(query)
    elif "help_command"    in query: help_command(query)
    elif query == "get_count_phone" : print(get_count_phone())
    elif query == "get_forbiddens"  : print(get_forbiddens())
    elif query == "get_count"       : print(get_count())
    elif query == "phone_password"  : print_phone_password()
    elif query == "get_free_opens"  : print(get_free_opens())
    query = input("enter new input: ")

print("aplication is closed")
