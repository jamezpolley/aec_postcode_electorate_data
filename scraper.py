# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import requests
import os
from bs4 import BeautifulSoup

os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki

def scrape_postcode(postcode):
    urltemplate = "https://electorate.aec.gov.au/LocalitySearchResults.aspx?filter={}&filterby=Postcode"
    url = str.format(urltemplate, postcode)
    pageno = 1
    page = requests.get(url).content

    while True:
        bs4 = BeautifulSoup(page, "html.parser")

        rows = bs4.find(id='ContentPlaceHolderBody_gridViewLocalities').find_all('tr', recursive=False)

        for row in rows:
            # Skip header and footer of table because they're making tables like it's the 2000s
            if row.attrs == {}:
                tds = row.find_all('td')
                rowdata = {'state': tds[0].text, 'suburb': tds[1].text, 'postcode': tds[2].text, 'electorate': tds[3].text, 'redistributed': tds[4].text, 'other': tds[5].text}
                print(rowdata)
                scraperwiki.sqlite.save(unique_keys=('state', 'suburb', 'postcode', 'electorate'), data=rowdata, table_name='data')

        print(len(rows))
        if len(rows) < 22:
            return

        pageno += 1

        # Get the next page using the ASP.net postback
        data = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolderBody$gridViewLocalities",
            "__EVENTARGUMENT": "Page${}".format(pageno),
        	"__VIEWSTATEENCRYPTED": "",
            "__VIEWSTATE": bs4.find(id="__VIEWSTATE")["value"],
            "__VIEWSTATEGENERATOR": bs4.find(id="__VIEWSTATEGENERATOR")["value"],
            "__EVENTVALIDATION": bs4.find(id="__EVENTVALIDATION")["value"],
        }
        page = requests.post(url, data=data).content

# Oh lordy. The AEC website appears to be blocking morph.io.
# Use our proxy if the MORPH_AUSTRALIAN_PROXY environment variable is set
if "MORPH_AUSTRALIAN_PROXY" in os.environ:
    print("Using proxy setting in MORPH_AUSTRALIAN_PROXY...")
    os.environ['HTTP_PROXY'] = os.environ['MORPH_AUSTRALIAN_PROXY']
    os.environ['HTTPS_PROXY'] = os.environ['MORPH_AUSTRALIAN_PROXY']

postcodes = open("postcodes", "r").readlines()
total_codes = len(postcodes)
i = 0
for postcode in postcodes:
    i+=1
    postcode = postcode.strip()
    print("{}: {}/{}".format(postcode, i, total_codes))
    scrape_postcode(postcode)
