from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re

department_url = 'https://catalog.unc.edu/courses/'

req = Request(department_url, headers={'User-Agent':'Mozilla/5.0'})

webpage = urlopen(req).read()

page_soup = soup(webpage,"html.parser")

containers = page_soup.body.find_all("a", href = re.compile("courses"))

filename = "Department.csv"
f = open(filename, "w")
headers = "link, name, code\n"
f.write(headers)

department_list = [0] * 10
for container in containers:
    department_link = container['href']
    department_list = container.text.strip().split("(")
    department_name = "\"%s\"" % department_list[0]
    if(len(department_list) == 1):
        department_list.append('N/A')
    department_code = department_list[1][:-1]
    f.write(department_link + "," + department_name + "," + department_code + "\n")

f.close
    