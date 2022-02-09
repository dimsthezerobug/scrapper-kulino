import os
import requests
import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")


class Absenno:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.url = "https://kulino.dinus.ac.id/"
        self.login()

    def login(self):
        # ke kulino
        respond = self.session.get(url=self.url, verify=False)

        # cari token
        soup = BeautifulSoup(respond.text, "html.parser")
        token = soup.select_one("#block-login > input:nth-child(3)").get("value")

        # login
        data = {'anchor': '', 'logintoken': token, 'username': self.username, 'password': self.password}
        self.session.post(url=self.url + "/login/index.php", data=data)

    def getDashboard(self):
        respond = self.session.get("https://kulino.dinus.ac.id/my/")
        content = respond.text

        return content

    def getName(self):
        dashboard_content = self.getDashboard()
        soup = BeautifulSoup(dashboard_content, "html.parser")
        name = (soup.select_one(".usertext").string).split(" - ")[-1]

        return name

    def getCourses(self):
        dashboard_content = self.getDashboard()
        soup = BeautifulSoup(dashboard_content, "html.parser")

        courses = {}
        for course in soup.select(".type_course.depth_3"):
            course_id = course.find("p")["data-node-key"]
            course_name = course.find("a")["title"][8:]
            courses[course_name] = course_id

        return courses


def main():
    username = os.environ["username_kul"]
    password = os.environ["password_kul"]

    absen = Absenno(username, password)
    print(absen.getName())
    print(absen.getCourses())


if __name__ == "__main__":
    main()
