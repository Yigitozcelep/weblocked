import webbrowser
import keyring
import datetime
import pexpect
import time

initial_date = datetime.datetime.strptime("2024-06-07 00:00:00", "%Y-%m-%d %H:%M:%S")

keyring_date_data_service             = ""
keyring_date_data_username            = ""

keyring_terminal_password_service     = ""
keyring_terminal_password_username    = ""

keyring_phone_password_service        = ""
keyring_phone_password_username       = ""

keyring_forbidden_address_service     = ""
keyring_forbidden_address_username    = ""

keyring_accessible_days_service       = ""
keyring_accessible_days_username      = ""

keyring_last_open_service             = ""       
keyring_last_open_username            = ""

current_service_data = "3" * 1000
##current_password = "01MAx=asd,!0MxzASDomzxcAP3#[a=1230X(masdp>Sdm23-"


def delete_keyrings():
    if keyring.get_password(keyring_date_data_service, keyring_date_data_username):
        keyring.delete_password(keyring_date_data_service, keyring_date_data_username)

    if keyring.get_password(keyring_terminal_password_service, keyring_terminal_password_username):
        keyring.delete_password(keyring_terminal_password_service, keyring_terminal_password_username)

    if keyring.get_password(keyring_phone_password_service, keyring_phone_password_username):
        keyring.delete_password(keyring_phone_password_service, keyring_phone_password_username)
    
    if keyring.get_password(keyring_forbidden_address_service, keyring_forbidden_address_username):
        keyring.delete_password(keyring_forbidden_address_service, keyring_forbidden_address_username)

    if keyring.get_password(keyring_accessible_days_service, keyring_accessible_days_username):
        keyring.delete_password(keyring_accessible_days_service, keyring_accessible_days_username)

    if keyring.get_password(keyring_last_open_service, keyring_last_open_username):
        keyring.delete_password(keyring_last_open_service, keyring_last_open_username)


def initialize_app():
    if not keyring.get_password(keyring_date_data_service, keyring_date_data_username):
        keyring.set_password(keyring_date_data_service, keyring_date_data_username, current_service_data)
    
    if not keyring.get_password(keyring_terminal_password_service, keyring_terminal_password_username):
        set_new_terminal_password()

    if not keyring.get_password(keyring_last_open_service, keyring_last_open_username):
        keyring.set_password(keyring_last_open_service, keyring_last_open_username, str(datetime.datetime.today() - datetime.timedelta(100)))

    if not keyring.get_password(keyring_accessible_days_service, keyring_accessible_days_username):
        while True:
            print("this set new open date example 0:12-40 6:10-30 you can set any 2 time interval during that time restriction application can be used")
            query = input("enter open date: ")
            if query.count(" ") != 1:
                print(f"wrong input format 2 day should be entered")
                continue
            
            day1, day2 = query.split(" ")
            if not check_interval_format(day1) or not check_interval_format(day2): continue
            save_open_format(day1, day2)
            break
    


INITIAL_ETC_HOSTS_TEXT = """##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1    localhost
255.255.255.255    broadcasthost
::1    localhost


"""


def get_terminal_password():
    return keyring.get_password(keyring_terminal_password_service, keyring_terminal_password_username)


def calc_month_dif(d1, d2):
    return abs(12 * (d1.year - d2.year) + (d1.month - d2.month))

def get_initial_today_month_dif():
    return int(calc_month_dif(datetime.datetime.today(), initial_date))


def run_command(query):
    if query.count(" ") != 1:
        print("invalid format")
        return
    
    if not query.split(" ")[1]:
        print("invalid format empty address")
        return
    
    if "etc/hosts" in query:
        print("weblocked progrem error etc/hosts can not be in query")
        return
    if ".sh" in query:
        print("weblocked do not allowed to run .sh file")
        return  

    command = " ".join(query.split(" ")[1:])
    child = pexpect.spawn(command)
    index = child.expect([".?[Pp]assword:?.?", pexpect.EOF, pexpect.TIMEOUT])
    if index == 0: child.sendline(get_terminal_password())
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
    last_visited = get_last_visit()
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
    
    if not is_free_open_interval(): 
        decrement_count()
        keyring.set_password(keyring_last_open_service, keyring_last_open_username, str(datetime.datetime.today()))
    
    data = query.split(" ")[1:]

    delete_etc_hosts()
    for asked_adresses in data:
        webbrowser.open(asked_adresses)
    
    save_keyring_to_etc_hosts()
    

def add_forbidden(query):
    if query.count(" ") != 1:
        print("wrong input format")
        return
    data = query.split(" ")
    if len(data) != 2:
        print("wrong input format it should be written like add_forbidden www.youtube.com")
        return
    
    address = data[1]
    if not address:
        print("wrong input format empty address")
        return
    
    forbiddens = get_forbiddens() or ""
    if forbiddens and forbiddens.split("|").count(address):
        print("wrong input address already in database")
        return
    
    keyring.set_password(keyring_forbidden_address_service, keyring_forbidden_address_username, forbiddens + "|" + address)
    save_keyring_to_etc_hosts()


def save_keyring_to_etc_hosts():
    prev_forbiddens = get_forbiddens() or ""
    text = INITIAL_ETC_HOSTS_TEXT
    for address in prev_forbiddens.split("|")[1:]:
        text += f"127.0.0.1 {address}\n"
    
    command = f"echo '{text}' | sudo tee /etc/hosts"
    child = pexpect.spawn('/bin/bash', ['-c', command])
    index = child.expect(["Password:", pexpect.EOF, pexpect.TIMEOUT])
    if index == 0: child.sendline(get_terminal_password())
    child.interact()
    print("/etc/hosts sucessfully updated")

def get_forbiddens():
    return keyring.get_password(keyring_forbidden_address_service, keyring_forbidden_address_username)


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
    count = get_count()
    if not is_free_open_interval() and count <= 0 :
        print("your count is 0 you can not open forbidden application")
        return
    
    if not is_free_open_interval(): 
        decrement_count()
        keyring.set_password(keyring_last_open_service, keyring_last_open_username, str(datetime.datetime.today()))


    print("password: ", keyring.get_password(keyring_phone_password_service, keyring_phone_password_username))


def check_interval_format(d):
    if len(d) != 7: print(f"wrong input format {d} your input length should be 7")
    elif d[1] != ":" or d[4] != "-": print(f"wrong input format {d} input should contain ':' and '-' for example 5:12-40")
    elif not d[0].isnumeric() or not d[2].isnumeric() or not d[3].isnumeric() or not d[5].isnumeric() or not d[6].isnumeric(): print(f"wrong input format {d} day format should be numeric")
    elif int(d[2] + d[3]) > 24 or int(d[5] + d[6]) > 60: print(f"wrong input format {d} hour should not be more than 24 and minute should not be more than 60")
    else: return True
    return False

def save_open_format(day1, day2):
    keyring.set_password(keyring_accessible_days_service, keyring_accessible_days_username, day1 + "|" + day2)


def set_new_open(query):
    if query.count(" ") != 2:
        print(f"wrong input format 2 day should be entered")
        return
    
    _, day1, day2 = query.split(" ")
    if not check_interval_format(day1) or not check_interval_format(day2): return
    if not is_free_open_interval() and get_count() <= 0 :
        print("your count is 0 you can not open forbidden application")
        return
    
    if not is_free_open_interval():
        decrement_count()
        keyring.set_password(keyring_last_open_service, keyring_last_open_username, str(datetime.datetime.today()))

    
    save_open_format()
    print("new day is successfully updated")


def delete_etc_hosts():
    text = INITIAL_ETC_HOSTS_TEXT
    command = f"echo '{text}' | sudo tee /etc/hosts"
    child = pexpect.spawn('/bin/bash', ['-c', command])
    index = child.expect(["Password:", pexpect.EOF, pexpect.TIMEOUT])
    if index == 0: child.sendline(get_terminal_password())
    child.interact()


def get_last_visit():
    last_visited = keyring.get_password(keyring_last_open_service, keyring_last_open_username)
    last_visited = datetime.datetime.strptime(last_visited, "%Y-%m-%d %H:%M:%S.%f")
    return last_visited

def print_info():
    print("""
    this application is used for set password for /etc/hosts folder to set limits to accessing the applications you added.
    first you need to set a strong complicated password that you can't remember\n    then you should open system settings users & groups then add automaticly login as
    also you need to login options in system settings and 'required password after screen saver begins or display is turned of' to never 
    now you can add application that you do not want to visited them outside of the time intervals you setted
    you can set time intervals using set_new_open you can visited with in 1 hour from beggining of time interval
    you have 3 visits outside of this time interval and you can open any application
    when you visit application using your open it decreases and\n    when it reach 0 you can not visit freely also you can visit any applicaiton with in 1 hour from your last open
    you can see your visit count you can visit outside of the time interval using get_count
    since you dont know your password you can run commands with sudo using run command
          """)

def help_command(query):
    if (query.count(" ") != 1):
        print("wrong input format there is no command example you need to write help get_count")
        return
    
    data = query.split(" ")[1]
    match data:
        case "run"              : print("if command need a password the run command automaticly enter the password there are limitiatons\nif only first input is password the application can automaticly write the password for example the application ask [y/n] question than asks password the application can not write password\nexample usage run sudo brew install something")
        case "get_count"        : print("the upper bound of get count is 3, it resets every month, with the count you have you can open any restricted application you want\nwhen you open a restricted application outside the setted time interval your count decrease by 1, when you have 0 count you can not open restricted applicaiton outside of time interval")
        case "open_forbiddens"  : print("open restricted application, you can add new restriction by using add_forbidden. Example usage open_forbiddens ww.youtube.com/watch?v=wX9cJ6t8IdI")
        case "get_forbiddens"   : print("get restricted applications and print them")
        case "get_free_opens"   : print("print the free open intervals, in that time intervals you can open any restricted application using open_forbiddens and your open count is not affected")
        case "set_new_open"     : print("you can set any 2 time interval during that time restriction application can be used, also using this decrease your open count by 1, so you have 0 count than you can not use this command")
        case "add_forbidden"    : print("add new restricted application to the database, the restricted application can not be deleted or modified so be carefull when adding new application")
        case "phone_password"   : print("show your phone password, it also use open count so you do not have enough open count you can not see your password")
        case "set phone"        : print("set phone password it can be changed it does not affect on open count you can freely change phone password")
        case "get_last_visit"   : print("prints the last open time outside of the free open intervals you can do anything such as run or open_forbiddens with in 1 hour of last visit freely")
        case "info"             : print("give general info about the application")

def set_new_terminal_password():
    print("this password should be same as the sudo password and you can not change the password after that this password will be used to make sudo commands in the terminal")
    while True:
        data = input("enter password: ")
        if data.count(" "):
            print("wrong input format password can't have space")
            continue

        if not data:
            print("wrong input format empty password")
            continue
        
        keyring.set_password(keyring_terminal_password_service, keyring_terminal_password_username, data)
        print("password is successfully initialized")
        return

def set_phone(query):
    if query.count(" ") != 1:
        print("wrong input format")
        return
    
    data = query.split(" ")[1]
    if not data:
        print("wrong input format empty password")
        return
    
    keyring.set_password(keyring_phone_password_service, keyring_phone_password_username, data)
    print("phone password successfully updated")
    
        

def start():
    print("\n+------------------------------------ Commands ------------------------------------+")
    print("| run             \\\ run command and enter password if needed run rm -rf xx        |")
    print("| add_forbidden   \\\ example usage add_forbidden www.youtube.com                   |")
    print("| open_forbiddens \\\ open_forbiddens https://www.youtube.com/watch?v=DL6lAk4r      |")
    print("| get_forbiddens  \\\ get names of forbidden applications                           |")
    print("| get_count       \\\ get count of the urgent open for this month                   |")
    print("| get_free_opens  \\\ get days hours of free open                                   |")
    print("| set_new_open    \\\ this set new open date example set_new_open 0:12-40 6:10-30   |")
    print("| phone_password  \\\ show the phone password                                       |")
    print("| set_phone       \\\ set phone password it can be changed                          |")
    print("| get_last_visit  \\\ you can open freely anything 1hour range in last_open         |")
    print("| info            \\\ give general info about how to use application                |")
    print("| help_command    \\\ examples help run or help open it gives detailed explanation  |")
    print("| quit(q)         \\\ quit from application                                         |")
    print("+----------------------------------------------------------------------------------+")

    query = input("enter input: ")
    while query != "q" and query != "quit":
        if   "help_command"    in query: help_command(query)
        elif "run"             in query: run_command(query)
        elif "set_new_open"    in query: set_new_open(query)
        elif "open_forbiddens" in query: open_forbiddens(query)
        elif "add_forbidden"   in query: add_forbidden(query)
        elif "set_phone"       in query: set_phone(query)
        elif query == "get_forbiddens"  : print(get_forbiddens())
        elif query == "get_count"       : print(get_count())
        elif query == "phone_password"  : print_phone_password()
        elif query == "get_free_opens"  : print(get_free_opens())
        elif query == "info"            : print_info()
        elif query == "get_last_visit"  : print(get_last_visit())
        else: print(f"the command is not found: {query}")
        query = input("enter new input: ")

    print("aplication is closed")


initialize_app()
start()
