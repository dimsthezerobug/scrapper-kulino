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
        self.targets = []
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

    def showCourses(self):
        courses = self.getCourses()
        for course, id in courses.items():
            print(id, "-", course)

    def setTarget(self, id_course):
        self.targets.append(id_course)

    def absen(self):
        for target in self.targets:
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
                        print("[Closed]", forums[i].select_one("span.instancename").text)

                    i -= 1

                if discussion_id != "":
                    respond_discussion = self.session.get(self.url + "/mod/forum/discuss.php?d=" + discussion_id)
                    with open("discussion.html", "w", encoding="utf-8") as file:
                        file.write(respond_discussion.text)
                    soup_discussion = BeautifulSoup(respond_discussion.text, "html.parser")
                    question = soup_discussion.find(class_="starter").find("p").text
                    print("Pertanyaan: " + question)        


def main():
    username = os.environ["username_kul"]
    password = os.environ["password_kul"]

    absen = Absenno(username, password)
    print(absen.getName())
    # print(absen.getCourses())
    absen.showCourses()
    while True:
        absen.setTarget(input("Masukan kode matkul: "))
        absen.absen()


if __name__ == "__main__":
    main()
