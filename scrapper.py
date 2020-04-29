from requests import get
from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
import sys

company_code = sys.argv[1]

def get_company_url(code:str)->str:
    resp = post('https://rekvizitai.vz.lt/imones/1', {'name':'', 'city':0,'word':'','code':code,'catUrlKey':'','ok':'','resetFilter':0,'order':1})
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        return soup.find_all("div", class_="info")[0].find('a').get('href')
    else:
        return None

def get_url_content(code:str):
    with closing(get(get_company_url(code), stream=True)) as reply:
        if reply.status_code == 200:
            return reply.content
        else:
            return None
    
def write_json(company): 
    with open('data.json') as json_file: 
        data = json.load(json_file) 
      
    temp = data['companies'] 
    temp.append(company) 
      
    with open('companies.json','w') as f: 
        json.dump(data, f) 

def main():
	temp = get_url_content(company_code)
	print(temp)

if __name__ == "__main__":
    main()

