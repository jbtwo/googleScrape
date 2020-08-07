import re
import time
import urllib
import random
import numpy as np
import requests
from bs4 import BeautifulSoup
from site_list import sites

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
]

file_path = 'result.txt'

i = 1

for site in sites:
   
    # get+log timne of request
    currentTime = time.strftime("%H:%M:%S", time.localtime())
   
    # pick random user_agent
    user_agent = random.choice(user_agent_list)
   
    # set request headers
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": user_agent
    }
    
    # build search query from site_list
    query = f"site:{site}"
    
    # build url from query
    URL = f"https://google.com/search?q={query}"

    # store response
    resp = requests.get(URL, headers=headers)

    # sleep 1 hour if throttled
    if resp.status_code == 429:
        print(i, "-", currentTime, "Fuck we're throttled")
        i = i+1
        time.sleep(6000)

    # parse any 200 response
    elif resp.status_code == 200:
        print(i, "-", currentTime, site, resp.status_code)
        i = i+1
        soup = BeautifulSoup(resp.content, "html.parser")
        # store result-stats element contents
        temp1 = soup.find(id="result-stats")
        
        if temp1:
            # extract text from element
            temp2 = temp1.get_text()
            # regex out integer from result string
            result = re.search(r'(\d+)', temp2).group()
            # write result to new line in file
            with open(file_path, 'a') as file:
                file.write(result + ' ' + site + '\n')
        # wait between 5 to 16 seconds (chosen randomly)
        time.sleep((16-5)*np.random.random()+5) 
    #log error
    else:
        print(i, "-", currentTime, r"non 200/429 ¯\_(ツ)_/¯")
        i = i + 1
