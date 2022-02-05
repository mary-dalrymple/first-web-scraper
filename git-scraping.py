# Proposed Git Scraping Website
# https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf

# This website contains two sources of newsworthy information 
# that could be mined to better communicate the information:
# 1. Reported breaches of protected health information under 
#    investigation
# 2. Investigation outcomes of prior reported breaches 

# Reasons to scrape for a news app:
# * Early alert system for affected patients
# * Put in a location consumers can actually find and use
# * Aggregate trends - total individuals effected, most common 
#   types of beaches, location of breached information
# * As far as I can tell, this may be the only real big picture
#   accounting of ransomware in health care (which is a 
#   major and growing problem and a per se violation of health 
#   data protection rules)
# * Accounting of how many disclosures due to external forces
#   like hacking/ransomware or theft vs internal bad actors
#   or process controls (unauthorized access) 
# * Candidate for git scraping to keep up with new addition
#   and resolution of cases under investigation

import csv
import requests
from bs4 import BeautifulSoup

# successfully grabs website
url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = response.content
# print(html)

soup = BeautifulSoup(html, features="html.parser")
# print(soup.prettify())

table = soup.find(id = 'ocrForm:reportResultTable_data')
# print(table.prettify())

# using declared role instead of <tr> tag for clarity
# for row in table.find_all(role = 'row'):
#     print(row.prettify())

# dude! worked, and no funkiness in the cell with the toggle arrow
# for row in table.find_all(role = 'row'):
#     for cell in row.find_all('td'):
#         print(cell.text)

list_of_rows = []
for row in table.find_all(role = 'row'):
    list_of_cells = []
    for cell in row.find_all('td'):
        text = cell.text.strip() 
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells[1:9]) # drop index 0 for UI toggle

# print(list_of_rows)

outfile = open("./hipaa_cases.csv", "w", newline='') # add newline for Windows, fix alternating empty row problem
writer = csv.writer(outfile)
# adds headers for hidden cols
writer.writerow(["covered_entity", "state", "covered_entity_type", "num_affected", "submission_date", "breach_type", "breached_info_location", "biz_assoc", "description"]) # add header row
writer.writerows(list_of_rows)

# This scrapes the cases under investigation list (hooray!).
# Next steps:
# 1. This grabs the first 100 records. IRL, I'd probably 
# do a manual grab of the base set and then use the scraper
# to update new stuff, so maybe no need to go past the first
# 100 records.
# 2. would be to figure out how to trigger the archive
# button and grab the resolved cases separately. Both go to 
# the same .jsf URL.
# 3. If automated, dedupe repeated rows if can't do full data
# grab every time.