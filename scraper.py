# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import requests
import os
from bs4 import BeautifulSoup

os.environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki


urltemplate = "https://electorate.aec.gov.au/LocalitySearchResults.aspx?filter={}&filterby=Postcode"
postcodes = open("postcodes", "r").readlines()
total_codes = len(postcodes)
i = 0
for postcode in postcodes:
    i+=1
    postcode = postcode.strip()
    print("{}: {}/{}".format(postcode, i, total_codes))
    url = str.format(urltemplate, postcode)

    page = requests.get(url).content
    print(page)
    bs4 = BeautifulSoup(page, "html.parser")

    rows = bs4.find(id='ContentPlaceHolderBody_gridViewLocalities').find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 6:
            rowdata = {'state': tds[0].text, 'suburb': tds[1].text, 'postcode': tds[2].text, 'electorate': tds[3].text, 'redistributed': tds[4].text, 'other': tds[5].text}
            scraperwiki.sqlite.save(unique_keys=('state', 'suburb', 'postcode', 'electorate'), data=rowdata, table_name='data')
