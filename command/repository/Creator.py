#!python3
#encoding:utf-8
import subprocess
import shlex
import datetime
import time
import pytz
import requests
import json
import Data

class Creator:
    def __init__(self, data):
        self.data = data

    def Create(self):
        self.__CreateLocalRepository()
        j = self.__CreateRemoteRepository()
        self.__InsertRemoteRepository(j)

    def __CreateLocalRepository(self):
        subprocess.call(shlex.split("git init"))
        subprocess.call(shlex.split("git config --local user.name '{0}'".format(self.data.get_username())))
        subprocess.call(shlex.split("git config --local user.email '{0}'".format(self.data.get_mail_address())))
        subprocess.call(shlex.split("git remote add origin git@{0}:{1}/{2}.git".format(self.data.get_ssh_host(), self.data.get_username(), self.data.get_repo_name())))

    def __CreateRemoteRepository(self):
        url = 'https://api.github.com/user/repos'
        post_data = json.dumps({"name": self.data.get_repo_name(), "description": self.data.get_repo_description(), "homepage": self.data.get_repo_homepage()})
        headers={
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token(['repo']))
        }
        r = requests.post(url, data=post_data, headers=headers)
        print(r.text)
        time.sleep(2)
        return json.loads(r.text)

    def __InsertRemoteRepository(self, j):
        self.data.db_repo.begin()
        repo = self.data.db_repo['Repositories'].find_one(Name=j['name'])
        # Repositoriesテーブルに挿入する
        if None is repo:
            self.data.db_repo['Repositories'].insert(self.__CreateRecordRepositories(j))
            repo = self.data.db_repo['Repositories'].find_one(Name=j['name'])
        # 何らかの原因でローカルDBに既存の場合はそのレコードを更新する
        else:
            self.data.db_repo['Repositories'].update(self.__CreateRecordRepositories(j), ['Name'])

        # Countsテーブルに挿入する
        cnt = self.data.db_repo['Counts'].count(RepositoryId=repo['Id'])
        if 0 == cnt:
            self.data.db_repo['Counts'].insert(self.__CreateRecordCounts(self.data.db_repo['Repositories'].find_one(Name=j['name'])['Id'], j))
        # 何らかの原因でローカルDBに既存の場合はそのレコードを更新する
        else:
            self.data.db_repo['Counts'].update(self.__CreateRecordCounts(repo['Id'], j), ['RepositoryId'])
        self.data.db_repo.commit()

    def __CreateRecordRepositories(self, j):
        return dict(
            IdOnGitHub=j['id'],
            Name=j['name'],
            Description=j['description'],
            Homepage=j['homepage'],
            CreatedAt=j['created_at'],
            PushedAt=j['pushed_at'],
            UpdatedAt=j['updated_at'],
            CheckedAt="{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc))
        )

    def __CreateRecordCounts(self, repo_id, j):
        return dict(
            RepositoryId=repo_id,
            Forks=j['forks_count'],
            Stargazers=j['stargazers_count'],
            Watchers=j['watchers_count'],
            Issues=j['open_issues_count']
        )

