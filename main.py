import requests
from bs4 import BeautifulSoup

URL = "https://kulino.dinus.ac.id/"

with open("account.txt") as file:
    account = file.readline().split()

username = account[0]
password = account[1]
session = requests.Session()


def login():
    # masuk kulino
    respond = session.get(url=URL)

    # cari token
    soup = BeautifulSoup(respond.text, "html.parser")
    token = soup.select_one("#block-login > input:nth-child(3)").get("value")
    # print(token)

    # login ke kulino
    data = {'anchor': '', 'logintoken': token, 'username': username, 'password': password,}
    respond_2 = session.post(url=URL + "/login/index.php", data=data)

    # dashboard
    respond_3 = session.get("https://kulino.dinus.ac.id/my/")
    dashboard_content = respond_3.text
    soup_dashboard = BeautifulSoup(dashboard_content, "html.parser")
    nim_name = (soup_dashboard.select_one(".usertext").string).split(' - ')
    NAME = nim_name[-1]

    print(f"SELAMAT DATANG DI ABSENNO {NAME}\n")

    return dashboard_content


def change_acct():
    username = input("\nMasukan username: ")
    password = input("Masukan password: ")
    
    with open("account.txt", mode="w") as file:
        file.write(f"{username} {password}")
       
    print("\nAkun Telah Diganti")


def main():
    dashboard_content = login()

    # tampilan menu
    print("Daftar Menu: ")
    print("\n1. Absensi\n2. Cek Absensi\n3. Pindah Akun\n")
    try:
        order = int(input("Silahkan pilih menu (masukan angka 1/2/3) : "))
    except:
        print("Terjadi Kesalahan")
       
    if order == 1:
        pass
    elif order == 2:
        pass
    elif order == 3:
        change_acct()
    else:
        print("Terjadi Kesalahan")
  

if __name__ == "__main__":
    main()
