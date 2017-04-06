#!python3
#encoding:utf-8
import os
import Data
import time
import pytz
import requests
import json
import datetime

class Editor:
    def __init__(self, data):
        self.data = data

    def Edit(self, name, description, homepage):
        j = self.__EditRemoteRepository(name, description, homepage)
        self.__EditDb(j)
        # リポジトリ名の変更が成功したら、ディレクトリ名も変更する
        if self.data.get_repo_name() != name:
            os.rename("../" + self.data.get_repo_name(), "../" + name)

    def __EditRemoteRepository(self, name, description, homepage):
        # リポジトリ名は必須
        url = 'https://api.github.com/repos/{0}/{1}'.format(self.data.get_username(), self.data.get_repo_name())
        headers={
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token())
        }
        data = {}
        data['name'] = name
        if not(None is description or '' == description):
            data['description'] = description
        if not(None is homepage or '' == homepage):
            data['homepage'] = homepage

        r = requests.patch(url, headers=headers, data=json.dumps(data))
        if 200 != r.status_code:
            raise Exception('HTTPエラー: {0}'.format(r.status_code))
        time.sleep(2)
        return json.loads(r.text)

    def __EditDb(self, j):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        data = {}
        data['Id'] = repo['Id']
        data['Name'] = j['name']
        if not(None is j['description'] or '' == j['description']):
            data['Description'] = j['description']
        if not(None is j['homepage'] or '' == j['homepage']):
            data['Homepage'] = j['homepage']
        data['CreatedAt']=j['created_at']
        data['PushedAt']=j['pushed_at']
        data['UpdatedAt']=j['updated_at']
        data['CheckedAt']="{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc))
        self.data.db_repo['Repositories'].update(data, ['Id'])
