# weblocked

installation guide
1) git clone the repository

2) change the variables randomly
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

you can write anystring inside of "" for example
keyring_date_data_service             = "ASDasdsadasd12d1d1d1"
keyring_date_data_username            = "12d1dSADmo1m2odmoSA"

keyring_terminal_password_service     = "12domOSAMdom12d"
keyring_terminal_password_username    = "SAOdmo12mdomsaDM"

keyring_phone_password_service        = "!Domsaodmasomd12"
keyring_phone_password_username       = "O!DM2odmoasd12o3"

keyring_forbidden_address_service     = "asdasdadoam12om"
keyring_forbidden_address_username    = "ASDm12odmo12"

keyring_accessible_days_service       = "31odm1o3do asd"
keyring_accessible_days_username      = "12o21odm1o2mdo13md"

keyring_last_open_service             = "21omdo1m3odm12"       
keyring_last_open_username            = "31om13od1m3odm1od1"


3) first you need to set a strong complicated password that you can't remembe then you should open system settings users & groups then add automaticly login as (make sure the you write password in some place you need that password in future steps)

4) open the application and enter the password you saved

5) $ pip install pyinstaller
   $ pip install keyring
   $ pip install pexpect
   $ brew install android-platform-tools
   





7) pyinstaller weblocked.py --distpath /Users/yigitozcelep/Desktop --onefile  ## you need to make location desktop because keyring can accessed only first bundled place so if you not specify the destination to desktop you can not use it in desktop

8) open the file, the operating system will ask you password multiple times due to the keyring you need to write the password

9) in first open application ask you the password and the dates you want to open restricted applications, you need to enter them

10) make sure that use every command in first open because keyring will ask you the password for access (only one time) click always allowed

11) for enter phone password automaticly,
    watch this video https://www.youtube.com/watch?v=We45D_TjKdc or write adb: no devices/emulators found to youtube.

    ayarlar(settings)->telefone hakkında(about phone) -> yazılım bilgileri -> 7 kere yapım numarasına tıkla -> ayarlara çık gir yap -> en aşağıda geliştirici seçenekleri -> uyanık kal ve usb hata ayıklaması nı aç
    passwordda ok ile onaylama olmucak bide onuda şifre belirlerken seçiceksin


13) connect phone to computer via usb cable (for wifi connection)
   $ adb devices
   $ adb tcpip 5555
   $ adb connect device_ip_address:5555 # go to phone wife goto setting of the current connected wifi in the bottom there is IP address like 192.30.5.90
   

