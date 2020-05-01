from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse
from requests import get
from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

def get_company_url(code:str)->str:
    """
    Method for retrieving URL in Rekvizitai.lt website of any commercial company in Lithunia by company code
    Arguments:
        code (str) -- Litnianian company code
    Returns:
        str -- ural of desired company
    """
    params = {'name':'', 'city':0,'word':'','code':code,'catUrlKey':'','ok':'','resetFilter':0,'order':1}
    url = "https://rekvizitai.vz.lt/imones/1"

    with closing(post(url, params)) as response:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.find_all("div", class_="info")[0].find('a').get('href')
        else:
            return None

def get_url_content(url:str):
    """
    Method returns raw html content from given url
    Arguments:
        url (str)
    Returns:
        str -- raw html from given url
    """
    with closing(get(url, stream=True)) as reply:
        if reply.status_code == 200:
            return reply.content
        else:
            return None

class Company(Resource):
    def post(self):
        """
        POST Request
        Arguments:
            {} -- company code egz.: {"code", "304232351"}
        Returns:
            {} -- parameters and values about requested company

        """
        json_data = request.get_json(force=True)
        if "code" not in json_data or len(json_data["code"]) != 9:
            return "Wrong parameter", 400

        raw_html = get_url_content(get_company_url(json_data["code"]))
        if raw_html == None or len(raw_html) == 0:
            return f"Company with code {json_data['code']} was not found", 400
            
        soup = BeautifulSoup(raw_html, 'html.parser')
        name = soup.find("div", class_="name floatLeft").find('h1').get_text()
        return name, 200

api.add_resource(Company, "/getdata/")
if __name__ == '__main__':
    app.run(debug=True)



    

