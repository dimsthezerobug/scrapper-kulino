import os
from absenno import Absenno
from datetime import datetime
from termcolor import colored


def main():

    USERNAME = os.environ["username_kul"]
    PASSWORD = os.environ["password_kul"]

    # monday = 0, sunday = 6
    JADWAL = {  0: ["3481", "3441"],
                1: ["3374", "3363"],
                2: ["3326", "3406"],
                3: ["3282"],
                4: ["3269"]
             }

    print("""
     _      ____    ____    _____   _   _   _   _    ___  
    / \    | __ )  / ___|  | ____| | \ | | | \ | |  / _ \ 
   / _ \   |  _ \  \___ \  |  _|   |  \| | |  \| | | | | |
  / ___ \  | |_) |  ___) | | |___  | |\  | | |\  | | |_| |
 /_/   \_\ |____/  |____/  |_____| |_| \_| |_| \_|  \___/ 
                                                          
""")

    day = datetime.today().weekday()
    day = 2

    today = Absenno(USERNAME, PASSWORD)
    print("[+] SELAMAT DATANG ", end="")
    today.whoami()

    print("\n[+] DAFTAR MATKUL\n")
    today.showCourses()

    print("\n")

    for id in JADWAL[day]:
        today.setTarget(id)
    today.absen()

    is_continue = True
    while is_continue:
        input("\n\nKlik Enter untuk Exit")
        is_continue = False


if __name__ == "__main__":
    main()
