import colorama
import os
import random
import requests
import warnings
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from termcolor import colored
from textwrap import fill

colorama.init()

warnings.filterwarnings("ignore")


class Absenno:
    def __init__(self, username, password):
        self.courses = {}
        self.name = ""
        self.url = "https://kulino.dinus.ac.id/"
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.targets = []
        self.login()
        self.getCourses()

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

    def whoami(self):
        if self.name == "":
            dashboard_content = self.getDashboard()
            soup = BeautifulSoup(dashboard_content, "html.parser")
            name = (soup.select_one(".usertext").string).split(" - ")[-1]
            self.name = name

        return self.name

    def getCourses(self):
        if len(self.courses) == 0:
            dashboard_content = self.getDashboard()
            soup = BeautifulSoup(dashboard_content, "html.parser")

            courses = {}

            for course in soup.select(".type_course.depth_3"):
                course_id = course.find("p")["data-node-key"]
                course_name = course.find("a")["title"][8:]
                courses[course_id] = course_name

            self.courses = courses

        return self.courses

    def showCourses(self):
        courses = self.getCourses()
        for id, course in courses.items():
            print("   ", id, "-", course)

    def setTarget(self, id_course):
        self.targets.append(id_course)

    def generateAnswer(self, soup_discussion):
        try:
            all_answer = soup_discussion.find_all(class_="text_to_html")
            answer = all_answer[random.randrange(len(all_answer) + 1)].text
        except:
            answer = "hadir"

        return answer

    def comment(self, komentar):
        pass

    def absen(self):
        for target in self.targets:
            print(colored(f"\n[+] ABSEN {self.courses[target]}\n", "yellow"))
            # masuk ke course
            respond_course = self.session.get(self.url + "/course/view.php?id=" + target)
            soup_course = BeautifulSoup(respond_course.text, "html.parser")

            # mencari forum terbaru
            forums = soup_course.find_all(class_="modtype_forum")
            if len(forums) > 1:
                discussion_id = ""
                forums = forums[1:]
                i = len(forums) - 1
                is_continue = True
                while is_continue:
                    if i == 0:
                        is_continue = False

                    forum_id = forums[i]["id"].split("-")[-1]

                    try:
                        respond_forum = self.session.get(self.url+"/mod/forum/view.php?id=" + forum_id)
                        soup_forum = BeautifulSoup(respond_forum.text, "html.parser")
                        discussion_id = soup_forum.select_one("tr.discussion")["data-discussionid"]
                        is_continue = False
                    except:
                        # print("    [Closed]", forums[i].select_one("span.instancename").text)
                        pass

                    i -= 1

                if discussion_id != "":
                    # NOTE : belum ada proses validasi apakah user sudah pernah komentar atau belum
                    respond_discussion = self.session.get(self.url + "/mod/forum/discuss.php?d=" + discussion_id)
                    soup_discussion = BeautifulSoup(respond_discussion.text, "html.parser")
                    question = soup_discussion.find(class_="starter").find("p").text
                    answer = self.generateAnswer(soup_discussion)
                    # print("    ["+colored("?", "blue") +"] " + question)
                    # print("    ["+colored("=", "green") +"]", answer)

                    q = PrettyTable()
                    q.border = False
                    q.header = False
                    q.add_row([colored("   [?]", "yellow"), fill(f"{question}", width=50)])
                    q.align = "l"

                    a = PrettyTable()
                    a.border = False
                    a.header = False
                    a.add_row([colored("   [=]", "yellow"), fill(f"{answer}", width=50)])
                    a.align = "l"

                    print(q)
                    print()
                    print(a)
                else:
                    print("    ["+colored("!", "red") +"] Tidak Ada Forum Yang Terbuka") 


def main():
    username = os.environ["username_kul"]
    password = os.environ["password_kul"]

    absen = Absenno(username, password)
    absen.whoami()
    # print(absen.getCourses())
    absen.showCourses()
    while True:
        absen.setTarget(input("Masukan kode matkul: "))
        absen.absen()


if __name__ == "__main__":
    main()
