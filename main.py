import webbrowser
import keyring
import datetime
import pexpect
import time

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

keyring_last_open_service             = "DASMdaosdmaoq0239012ASDmasdoazxc90asd123mASdzxc"       
keyring_last_open_username            = "Asdmzxcz01230asdazxcmCXzokad1m23019asd09SAmxcza"

current_service_data = "3" * 1000
##current_password = "01MAx=asd,!0MxzASDomzxcAP3#[a=1230X(masdp>Sdm23-"
current_password = '"+dd&!A:>l%?B+p;9/M5'
phone_password   = "phone_password1"

def calc_month_dif(d1, d2):
    return abs(12 * (d1.year - d2.year) + (d1.month - d2.month))

def get_initial_today_month_dif():
    return int(calc_month_dif(datetime.datetime.today(), initial_date))


def run_command(query):
    if "etc/hosts" in query:
        print("weblocked progrem error etc/hosts can not be in query")
        return
    if ".sh" in query:
        print("weblocked do not allowed to run .sh file")
        return
    
    command = " ".join(query.split(" ")[1:])
    child = pexpect.spawn(command)
    index = child.expect([".?[Pp]assword:?.?", pexpect.EOF, pexpect.TIMEOUT])
    if index == 0: child.sendline(current_password)
    child.interact()
    

def is_free_open_interval():
    s1, s2 = get_free_opens().split("|")
    def check_is_in_interval(s):
        today = datetime.datetime.today()
        if today.weekday() != int(s[0]): return False
        dif = (today.hour * 60 + today.minute) - (int(s[2] + s[3]) * 60 + int(s[5] + s[6]))
        if dif > 60 or dif < 0: return False
        return True
    
    if check_is_in_interval(s1) | check_is_in_interval(s2): return True
    last_visited = keyring.get_password(keyring_last_open_service, keyring_last_open_username)
    last_visited = datetime.datetime.strptime(last_visited, "%Y-%m-%d %H:%M:%S.%f")
    dif = datetime.datetime.today() - last_visited
    return dif < datetime.timedelta(minutes=60)


def open_forbiddens(query):
    count = get_count()
    if query.count(" ") < 1:
        print(f"invalid format {query}")
        return
    
    if not is_free_open_interval() and count <= 0 :
        print("your count is 0 you can not open forbidden application")
        return
    
    if not is_free_open_interval(): decrement_count()
    data = query.split(" ")[1:]

    forbiddens = get_forbiddens()
    if not forbiddens:
        print("database is empty")
        return
    
    forbiddens = forbiddens.split("[")[1:]
    delete_etc_hosts()
    for name in data:
        for forbidden_name, forbidden_address in forbiddens.split("|"):
            if name != forbidden_name: continue
            webbrowser.open("https://" + forbidden_address)
            break
    
    time.sleep(0.2)
    save_keyring_to_etc_hosts()
    

def add_forbidden(query):
    if query.count(" ") < 1:
        print("wrong input format")
        return
    data = query.split(" ")
    
    if len(data) != 2:
        print("wrong input format it should be written like add_forbidden xxx|xxx.com")
        return
    
    query = data[1]
    if query.count("|") != 1:
        print("wrong input format delimeter should be |")
        return
    
    name, address = query.split("|")
    if not name or not address:
        print("wrong input format empty name or empty address")
        return
    
    forbiddens = get_forbiddens() or ""
    if forbiddens:
        data = [el for part in forbiddens.split("[")[1:] for el in part.split("|") ]
        if data.count(address) or data.count(name):
            print("wrong input address or name already in database")
            return
    
    keyring.set_password(keyring_app_name_and_address_service, keyring_app_name_and_address_username, forbiddens + "[" + query)
    save_keyring_to_etc_hosts()

def save_keyring_to_etc_hosts():
    prev_forbiddens = get_forbiddens() or ""
    text = """##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1    localhost
255.255.255.255    broadcasthost
::1    localhost

"""
    if not prev_forbiddens:
        print("wrong input no prev_forbiddens are avaliable nothing to save")
        return

    for part in prev_forbiddens.split("[")[1:]:
        forbidden_name, forbidden_address = part.split("|")
        text += f"127.0.0.1 {forbidden_address}\n"

    command = f"echo '{text}' | sudo tee /etc/hosts"
    child = pexpect.spawn('/bin/bash', ['-c', command])
    index = child.expect(["Password:", pexpect.EOF, pexpect.TIMEOUT])
    if index == 0: child.sendline(current_password)
    child.interact()
    print("/etc/hosts sucessfully updated")


def get_count_phone():
    date_data = keyring.get_password(keyring_phone_data_service, keyring_phone_data_username)
    return int(date_data[get_initial_today_month_dif()])


def get_forbiddens():
    return keyring.get_password(keyring_app_name_and_address_service, keyring_app_name_and_address_username)


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
    if query.count(" ") != 2:
        print(f"wrong input format 2 day should be entered")
        return
    
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
    print("new day is successfully updated")


def delete_etc_hosts():
    pass

def help_command(query):
    pass

print("\n+------------------------------------ Commands ------------------------------------+")
print("| run             \\\ run command and enter password if needed run rm -rf xx        |")
print("| get_count       \\\ get count of the urgent open for this month                   |")
print("| open_forbiddens \\\ open the forbidden aplication example open all                |")
print("| get_forbiddens  \\\ get names of forbidden applications                           |")
print("| get_free_opens  \\\ get days hours of free open                                   |")
print("| set_new_open    \\\ this set new open date example set_new_open 0:12-40 6:10-30   |")
print("| add_forbidden   \\\ example usage add_forbidden youtube|www.youtube.com           |")
print("| get_count_phone \\\ get count of urgen open phone for this month                  |")
print("| phone_password  \\\ show the phone password                                       |")
print("| help_command    \\\ examples help run or help open it gives detailed explanation  |")
print("| quit(q)         \\\ quit from application                                         |")
print("+----------------------------------------------------------------------------------+")

query = input("enter input: ")
while query != "q" and query != "quit":
    if             "run"   in query: run_command(query)
    elif   "set_new_open"  in query: set_new_open(query)
    elif "open_forbiddens" in query: open_forbiddens(query)
    elif "add_forbidden"   in query: add_forbidden(query)
    elif "help_command"    in query: help_command(query)
    elif query == "get_count_phone" : print(get_count_phone())
    elif query == "get_forbiddens"  : print(get_forbiddens())
    elif query == "get_count"       : print(get_count())
    elif query == "phone_password"  : print_phone_password()
    elif query == "get_free_opens"  : print(get_free_opens())
    else: print(f"the command is not found: {query}")
    query = input("enter new input: ")

print("aplication is closed")
