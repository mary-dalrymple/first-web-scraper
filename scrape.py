# put imports at top of file
# adding user agent allows scrapee to know you're coming from a browser and be less likely to block you
# could even put name and email if you're going to scrape every day and you want someone to know you're a good actor

import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.ola.state.md.us/Search/Report?keyword=&agencyId=&dateFrom=&dateTo='
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = response.content
# print(html)

soup = BeautifulSoup(html, features="html.parser")
# print(soup.prettify())
# table = soup.find_all('tbody')
table = soup.find('tbody')
# print(table.prettify())

# for row in table.find_all('tr'):
#     print(row.prettify())

# for row in table.find_all('tr'):
#     for cell in row.find_all('td'):
#         print(cell.text)


# go back to the documentation to see the construction of this loop step by step
# shouldn't have to worry about empty cells here because iterating using the tags
list_of_rows = []
for row in table.find_all('tr'):
    list_of_cells = []
    for cell in row.find_all('td'):
        if cell.find('a'):
            list_of_cells.append("https://www.ola.state.md.us" + cell.find('a')['href'])
        text = cell.text.strip() # to be safe from empty cells, take off the .strip()
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

# print(list_of_rows)

# look up python's list comprehensions for fancy stuff

outfile = open("./reports.csv", "w", newline='') # add newline for Windows, fix alternating empty row problem
writer = csv.writer(outfile)
writer.writerow(["date", "type", "url", "title"]) # add header row
writer.writerows(list_of_rows)