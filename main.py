import os
from absenno import Absenno
from datetime import datetime
from termcolor import colored
import colorama

colorama.init()


def main():

    USERNAME = os.environ["username_kul"]
    PASSWORD = os.environ["password_kul"]

    # monday = 0, sunday = 6
    JADWAL = {  0: ["3441", "3374", "3363"],
                1: ["3374", "3363"],
                2: ["3326", "3406"],
                3: ["3282"],
                4: ["3269"]
             }

    print(colored("""
     _      ____    ____    _____   _   _   _   _    ___  
    / \    | __ )  / ___|  | ____| | \ | | | \ | |  / _ \ 
   / _ \   |  _ \  \___ \  |  _|   |  \| | |  \| | | | | |
  / ___ \  | |_) |  ___) | | |___  | |\  | | |\  | | |_| |
 /_/   \_\ |____/  |____/  |_____| |_| \_| |_| \_|  \___/ 
                                                          
""", "yellow"))

    day = datetime.today().weekday()
    day = 0

    today = Absenno(USERNAME, PASSWORD)
    print(colored("[+] SELAMAT DATANG", "yellow"), today.whoami())

    print(colored("\n[+] DAFTAR MATKUL\n", "yellow"))
    today.showCourses()

    print("\n")

    try:
        for id in JADWAL[day]:
            today.setTarget(id)
        today.absen()
    except:
        print(colored("[+] HARI INI TIDAK ADA MATKUL", "yellow"))

    is_continue = True
    while is_continue:
        print(colored("\n\n[+] KLIK ENTER UNTUK EXIT ", "yellow"), end="")
        input()
        is_continue = False


if __name__ == "__main__":
    main()
