import requests
import base64
import json
import os.path
from datetime import date, datetime


class ConfluenceClient:
    def __init__(self, url, username, password):
        self.base_url = url
        self.api_path = "wiki/rest/api/"
        self.username = username
        self.password = password

    def get(self, path, params):
        url = os.path.join(self.base_url, self.api_path, path)
        headers = {
            "Accept": "application/json",
        }
        r = requests.get(url, 
                params=params, 
                headers=headers, 
                auth=(self.username, self.password)
        )
        if r.status_code != 200:
            print (r.content)
            raise Exception("this is bad!")
        data = r.json()
        return data

    def post(self, path, params, data):
        url = os.path.join(self.base_url, self.api_path, path)
        headers = {
            "Content-Type": "application/json",
        }
        reqdata = json.dumps(data)
        r = requests.post(url, 
                params=params, 
                headers=headers, 
                auth=(self.username, self.password),
                data=reqdata)
        if r.status_code != 200:
            print (r.content)
            raise Exception("this is bad!")
        outdata = r.json()
        return outdata

    def put(self, path, params, data):
        url = os.path.join(self.base_url, self.api_path, path)
        headers = {
            "Content-Type": "application/json",
        }
        reqdata = json.dumps(data)
        r = requests.put(url, 
                params=params, 
                headers=headers, 
                auth=(self.username, self.password),
                data=reqdata)
        if r.status_code != 200:
            print (r.content)
            raise Exception("this is bad!")
        outdata = r.json()
        return outdata

    def check_date_format(self, datestr, nom):
        if datestr is None:
            return
        if not re.match(datestr, r"\d\d\d\d-\d\d-\d\d"):
            raise Exception("%s needs to be in the format 'yyyy-mm-dd'" % nom)

    def check_int(self, num, nom):
        if num is None:
            return
        if not isinstance(num, int):
            raise Exception("%s needs to be an integer" % nom)

    def get_content(self, 
            spaceKey, title, type, status, postingDay, 
            expand, start, limit):
        params = {}
        if hasattr(postingDay, 'strftime'):
            postingDay = postingDay.strftime("%Y-%m-%d")
        if isinstance(expand, list):
            expand = ",".join(expand)
        self.check_date_format(postingDay, "postingDay")
        self.check_int(start, 'start')
        self.check_int(limit, 'limit')
        for k in ['spaceKey', 'type', 'title', 'status', 
                'postingDay', 'expand', 'start', 'limit']:
            if locals()[k] is not None:
                params[k] = locals()[k]

        return self.get('content', params)

    def get_blog_pages(self, 
            spaceKey=None, title=None, 
            status=None, postingDay=None, expand=None, 
            start=None, limit=None):
        return self.get_content(
                spaceKey=spaceKey, title=title, type='blogpost', 
                status=status, postingDay=postingDay, expand=expand, 
                start=start, limit=limit)

    def get_page(self, title, 
            spaceKey=None, status=None, postingDay=None, expand=None, 
            start=None, limit=None):
        return self.get_content(
                spaceKey=spaceKey, title=title, type='page', 
                status=status, postingDay=postingDay, expand=expand, 
                start=start, limit=limit)

    def create_page(self, title, spaceKey, body_storage, parent_id=None):
        data = {
            'type': 'page',
            'title': title,
            'space': {
                'key': spaceKey
            },
            'body': {
                'storage': {
                    'value': body_storage,
                    'representation': 'storage'
                }
            }
        }
        if parent_id is not None:
            data['ancestors'] = [{'id': parent_id}]
        return self.post('content', params={}, data=data)

    def update_page(self, page_id, version, title, spaceKey=None, body_storage=None, parent_id=None):
        data = {
            'type': 'page',
            'version': {
                'number': version
            },
            'title': title,
        }
        if spaceKey is not None:
            data['space'] = {
                'key': spaceKey
            }
        if body_storage is not None:
            data['body'] = {
                'storage': {
                    'value': body_storage,
                    'representation': 'storage'
                }
            }
        if parent_id is not None:
            data['ancestors'] = [{'id': parent_id}]
        return self.put(os.path.join('content', page_id), params={}, data=data)


