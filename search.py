import re
import time
import urllib

import numpy as np
import requests
from bs4 import BeautifulSoup

from site_list import sites

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

# sites = ['compassionatech.myshopify.com','bigwallprints.com']
file_path = '/Users/justinbrown/src/github.com/pythontest/scrape_google/result.txt'

i = 1

for site in sites:

    currentTime = time.strftime("%H:%M:%S", time.localtime()) 

    query = f"site:{site}"
    
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 429:
        print(i,"-",currentTime,"Fuck we're throttled")
        i = i+1
        time.sleep(6000)
        

    elif resp.status_code == 200:
        print(i, "-", currentTime, resp.status_code)
        i = i+1
        soup = BeautifulSoup(resp.content, "html.parser")
        temp1 = soup.find(id="result-stats")
        if temp1:
            temp2 = temp1.get_text()

            # through regular expression
            result = re.search(r'(\d+)', temp2).group()

            with open(file_path, 'a') as file:
                # could be any text, appended @ the end of file
                file.write(result + ' ' + site + '\n')
        time.sleep((30-5)*np.random.random()+5)  #from 5 to 30 seconds

    else:
        print(i, "-", currentTime, r"non 200/429 ¯\_(ツ)_/¯")
        i = i + 1
    
