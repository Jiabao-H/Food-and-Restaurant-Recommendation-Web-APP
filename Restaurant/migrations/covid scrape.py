import requests as req
from bs4 import BeautifulSoup
import sqlite3 as lite

data_list = []  # will be a list of tuples, and each tuple is a city/community info


page = 'http://publichealth.lacounty.gov/media/coronavirus/locations.htm'  #url of la covid page
resp = req.get(page)
soup = BeautifulSoup(resp.content, 'html.parser')
main_table = soup.find_all('table', attrs={'class': 'table table-striped table-bordered table-sm sticky-enabled'})[0]

print(main_table)

tbody = main_table.find('tbody')
print(tbody)

trs = tbody.find_all('tr')
trs = trs[1:]
for tr in trs:
    data_list.append(tuple([td.get_text(strip=True) for td in tr.find_all('td')])[1:])

print(data_list)
conn = lite.connect('551project.db')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS covid_table''')
cur.execute('''CREATE TABLE covid_table(
                    area INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                    cases TEXT, 
                    case rate TEXT,
                    deaths TEXT,
                    deaths rate TEXT,
                    )''')
conn.commit()

### Put all info the data_list into covid_table###
conn = lite.connect('551project.db')
cur = conn.cursor()
for i in range(len(data_list)):
    cur.execute('INSERT INTO covid_table(area,cases,case rate,deaths,deaths rate) values(?,?,?,?);',data_list[i])
conn.commit()