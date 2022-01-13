from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
def scrape():
    headers = ["Star_name", "Distance", "Mass", "Radius"]
    dwarf_data = []
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            dwarf_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done 1")
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_dwarf_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
scrape()
for index, data in enumerate(dwarf_data):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")
final_dwarf_data = []
for index, data in enumerate(dwarf_data):
    new_dwarf_data_element = new_dwarf_data[index]
    new_dwarf_data_element = [elem.replace("\n", "") for elem in new_dwarf_data_element]
    new_dwarf_data_element = new_dwarf_data_element[:7]
    final_dwarf_data.append(data + new_dwarf_data_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_dwarf_data)