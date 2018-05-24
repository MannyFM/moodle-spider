# %%
import cookielib
import mechanize
import urllib
import os, os.path
import re
from ConfigParser import ConfigParser
from bs4 import BeautifulSoup

# %%
conf = ConfigParser()
project_dir = os.getcwd()
conf.read(os.path.join(project_dir, 'config.ini'))

root_directory = conf.get("dirs", "root_dir").strip('\'"')
username = conf.get("auth", "username").strip('\'"')
password = conf.get("auth", "password").strip('\'"')
authentication_url = conf.get("auth", "url").strip('\'"')

if not root_directory.endswith("/"):
    root_directory += "/"

# %%
cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open(authentication_url)

br.select_form(nr=0)
br.form['username'] = username
br.form['password'] = password
br.submit()

contents = br.response().read()
if "My courses" not in contents:
    print("Cannot connect to moodle")
    exit(1)
print("Successfully authorized")

# %%
courses = contents.split("My courses</span></p>")[1]
courses = courses.split('</ul>')[0]
print(courses)

# %%
regex = re.compile('<a title="(.*?)" href="(.*?)">(.*?)</a>')
course_list = regex.findall(courses)
print course_list

# %%
def download_file(link, directory):
    print "downloading %s" % (link, )
    if "view.php?id=" in link:
        br.open(link)
        response = br.response().read()
        soup = BeautifulSoup(response, "html.parser")
        filelink = soup.find(class_="resourceworkaround").find("a").get("href")
    else:
        filelink = link
    filename = filelink.split("/")[-1]
    filename = urllib.unquote(filename)
    if os.path.exists(directory + filename):
        print "File already exists"
    else:
        file, _ = br.retrieve(filelink, directory + filename)

# %%
def parse_course(course_name, course_link, course_abbr):
    print "Parsing %s" % (course_name, )
    course_dir = root_directory + course_abbr + "/"
    if not os.path.isdir(course_dir):
        os.mkdir(course_dir)

    br.open(course_link)
    response = br.response().read()
    # print response
    soup = BeautifulSoup(response, "html.parser")
    links = soup.find(class_="weeks").find_all("a")
    for link in links:
        href = link.get('href')
        if "resource" not in href:
            # print "skipping link", href
            continue
        download_file(href, course_dir)

# %%
parse_course(course_list[2][0], course_list[2][1], course_list[2][2])

# %%
for name, link, abbr in course_list:
    parse_course(name, link, abbr)
