from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import pandas as pd

def main():   
    df = pd.read_csv('Department.csv')
    df.rename(columns={'link' : 'department_link', 'name': 'department_name', 'code': 'department_code'}, inplace = True)
    df.drop([0,1,2,294], inplace=True)
    bye = df.loc[df['department_link'] == '/courses/'].index
    df.drop(bye,inplace = True)
    df = df.reset_index(drop = True)
    length = len(df)
    for i in range(length):
        link = df._get_value(i,'department_link')
        code = link.partition("courses")[2][1:-1]
        each_department(link, code)

   
def each_department( link, code): 

    url = 'https://catalog.unc.edu' + link

    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})

    webpage = urlopen(req).read()

    page_soup = soup(webpage,"html.parser")

    containers = page_soup.body.find_all("div", attrs = {"class":"courseblock"})

    # len(containers) Check the length of the container

    # containers[0] Check the content of the container

    filename = code + ".csv"
    f = open(filename, "w")
    headers = "code, name, credit, desc, Prereqs, GenEd, Repeat, Grading\n"
    f.write(headers)


    for container in containers:
        class_info = container.find("p", attrs = {"class" : "courseblocktitle"}).text.split(".")
        class_code = class_info[0]
        class_name = "\"%s\"" % class_info[1]
        class_credit = re.sub("[^0-9]|-", "", class_info[2])

        class_desc = container.find("p", attrs = {"class" : "courseblockdesc"}).text
        list_1 = re.split('(Requisites: |Gen Ed: |Repeat rules: |Grading status: )', class_desc)
        class_right_desc = "\"%s\"" % list_1[0]
        length = len(list_1)
        class_req = ""
        class_gened = ""
        class_repeat = ""
        class_grading = ""
        for i in range(length):
            if(list_1[i] == "Requisites: "):
                class_req = "\"%s\"" % list_1[i+1]
            elif(list_1[i] == "Gen Ed: "):
                class_gened = "\"%s\"" % list_1[i+1]
            elif(list_1[i] == "Repeat rules: "):
                class_repeat = "\"%s\"" % list_1[i+1]
            elif(list_1[i] == "Grading status: "):
                class_grading = "\"%s\"" % list_1[i+1]
        
        f.write(class_code + "," + class_name + "," + class_credit + "," + class_right_desc + "," + class_req + "," + class_gened + "," + class_repeat + "," + class_grading + "\n")

    f.close
    return f
main()