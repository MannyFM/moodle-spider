# %%
import cookielib
import mechanize
import urllib
import os
import re
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)


# %%
def download_file(link, directory):
    global br
    if "view.php?id=" in link:
        br.open(link)
        response = br.response().read()
        soup = BeautifulSoup(response, "html.parser")
        file_link = soup.find(class_="resourceworkaround").find("a").get("href")
    else:
        file_link = link
    filename = file_link.split("/")[-1].split("?")[0]
    filename = urllib.unquote(filename)
    print "downloading %s" % (filename,)
    if os.path.exists(directory + filename):
        print "file already exists"
    else:
        br.retrieve(file_link, directory + filename)


def download_folder(link, directory):
    global br
    contents = br.open(link).read()
    soup = BeautifulSoup(contents, "html.parser")

    files = soup.find(class_="filemanager").find_all('a')
    foldername = soup.find(id="region-main").find('h2').text
    foldername = foldername.replace("/", "_")
    print "downloading folder %s" % (foldername,)

    folder_dir = directory + foldername + "/"
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)

    for link in files:
        print link.text
        href = link.get('href')
        download_file(href, folder_dir)


class Spider:
    def __init__(self, config_file="config.ini"):
        global br
        self.project_dir = os.getcwd()
        conf = ConfigParser()
        conf.read(os.path.join(self.project_dir, config_file))

        self.root_dir = conf.get("dirs", "root_dir").strip('\'"')
        self.username = conf.get("auth", "username").strip('\'"')
        self.password = conf.get("auth", "password").strip('\'"')
        self.auth_url = conf.get("auth", "url").strip('\'"')

        if not self.root_dir.endswith("/"):
            self.root_dir += "/"
        self.course_list = None

    def authorize_and_get_course_list(self):
        global br
        br.open(self.auth_url)
        br.select_form(nr=0)
        br.form['username'] = self.username
        br.form['password'] = self.password
        br.submit()

        contents = br.response().read()
        if "My courses" not in contents:
            print("cannot connect to moodle")
            return None
        print("successfully authorized")
        courses = contents.split("My courses</span></p>")[1]
        courses = courses.split('</ul>')[0]
        regex = re.compile('<a title="(.*?)" href="(.*?)">(.*?)</a>')
        self.course_list = regex.findall(courses)
        return self.course_list

    def parse_course_tuple(self, course_tuple):
        self.parse_course(course_tuple[0], course_tuple[1], course_tuple[2])

    def parse_course(self, course_name, course_link, course_abbr):
        global br
        print "parsing %s" % (course_name,)
        course_dir = self.root_dir + course_abbr + "/"
        if not os.path.isdir(course_dir):
            os.mkdir(course_dir)

        br.open(course_link)
        response = br.response().read()
        soup = BeautifulSoup(response, "html.parser")
        links = soup.find(class_="weeks").find_all("a")
        for link in links:
            href = link.get('href')
            if "resource" in href:
                download_file(href, course_dir)
            elif "folder" in href:
                download_folder(href, course_dir)
            else:
                print "unknown type of attachment:", href


# %%
def main():
    spider = Spider()
    course_list = spider.authorize_and_get_course_list()
    for course in course_list:
        spider.parse_course_tuple(course)


if __name__ == "__main__":
    main()
