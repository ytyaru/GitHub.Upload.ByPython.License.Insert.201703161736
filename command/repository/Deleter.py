#!python3
#encoding:utf-8
import os
import subprocess
import shlex
import shutil
import Data
import time
import pytz
import requests
import json
import datetime

class Deleter:
    def __init__(self, data):
        self.data = data

    def ShowDeleteRecords(self):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        print('Repositories-------')
        print(repo)
        print('Counts-------')
        print(self.data.db_repo['Counts'].find_one(RepositoryId=repo['Id']))
        print('Languages-------')
        for record in self.data.db_repo['Languages'].find(RepositoryId=repo['Id']):
            print(record)
        print('Licenses-------')
        print(self.data.db_repo['Licenses'].find_one(RepositoryId=repo['Id']))

    def Delete(self):
        self.__DeleteLocalRepository()
        self.__DeleteRemoteRepository()
        self.__DeleteDb()

    def __DeleteLocalRepository(self):
        shutil.rmtree('.git')

    def __DeleteRemoteRepository(self):
        url = 'https://api.github.com/repos/{0}/{1}'.format(self.data.get_username(), self.data.get_repo_name())
        headers={
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token(['delete_repo']))
        }
        r = requests.delete(url, headers=headers)
        if 204 != r.status_code:
            raise Exception('HTTPエラー: {0}'.format(status_code))
        time.sleep(2)

    def __DeleteDb(self):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        self.data.db_repo.begin()
        self.data.db_repo['Repositories'].delete(Id=repo['Id'])
        self.data.db_repo['Counts'].delete(RepositoryId=repo['Id'])
        self.data.db_repo['Languages'].delete(RepositoryId=repo['Id'])
        self.data.db_repo['Licenses'].delete(RepositoryId=repo['Id'])
        self.data.db_repo.commit()

