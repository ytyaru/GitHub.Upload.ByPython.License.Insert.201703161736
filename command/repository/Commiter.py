#!python3
#encoding:utf-8
import subprocess
import shlex
import time
import requests
import json
import Data

class Commiter:
    def __init__(self, data):
        self.data = data

    def ShowCommitFiles(self):
        subprocess.call(shlex.split("git add -n ."))

    def AddCommitPush(self, commit_message):
        subprocess.call(shlex.split("git add ."))
        subprocess.call(shlex.split("git commit -m '{0}'".format(commit_message)))
        subprocess.call(shlex.split("git push origin master"))
        time.sleep(3)
        self.__InsertLanguages(self.__GetLanguages())
        self.__InsertLicense()

    def __GetLanguages(self):
        url = 'https://api.github.com/repos/{0}/{1}/languages'.format(self.data.get_username(), self.data.get_repo_name())
        r = requests.get(url)
        if 300 <= r.status_code:
            print(r.status_code)
            print(r.text)
            print(url)
            raise Exception("HTTP Error {0}".format(r.status_code))
            return None
        else:
            print(r.text)
            return json.loads(r.text)

    def __InsertLanguages(self, j):
        self.data.db_repo.begin()
        repo_id = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())['Id']
        self.data.db_repo['Languages'].delete(RepositoryId=repo_id)
        for key in j.keys():
            self.data.db_repo['Languages'].insert(dict(
                RepositoryId=repo_id,
                Language=key,
                Size=j[key]
            ))
        self.data.db_repo.commit()

    def __InsertLicense(self):
        repo = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())
        if None is not repo:
            if None is not self.data.db_repo['Licenses'].find_one(RepositoryId=repo['Id']):
                # `LICENSE`,`LICENSE.txt`,`LICENSE.md`ファイルがgit addされているなら更新すべき。
                return
        time.sleep(2)
        # ライセンス情報を取得する
        j = self.__RequestRepository()
        if None is j['license']:
            license_id = None
        else:
            # マスターDBにないライセンスならAPIで取得する
            if None is self.data.db_license['Licenses'].find_one(Key=j['license']['key']):
                license = self.__RequestLicense(j['license']['key'])
                self.data.db_license['Licenses'].insert(self.__CreateRecordLicense(license))
            license_id = self.data.db_license['Licenses'].find_one(Key=j['license']['key'])['Id']
        # リポジトリとライセンスを紐付ける
        self.data.db_repo['Licenses'].insert(dict(
            RepositoryId=self.data.db_repo['Repositories'].find_one(IdOnGitHub=j['id'])['Id'],
            LicenseId=license_id
        ))

    def __RequestRepository(self):
        url = 'https://api.github.com/repos/{0}/{1}'.format(self.data.get_username(), self.data.get_repo_name())
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.__ReturnResponse(r, success_code=200)

    def __RequestLicense(self, key):
        url = 'https://api.github.com/licenses/' + key
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.__ReturnResponse(r, success_code=200)

    def __CreateRecordLicense(self, j):
        return dict(
            Key=j['key'],
            Name=j['name'],
            SpdxId=j['spdx_id'],
            Url=j['url'],
            HtmlUrl=j['html_url'],
            Featured=self.__BoolToInt(j['featured']),
            Description=j['description'],
            Implementation=j['implementation'],
            Permissions=self.__ArrayToString(j['permissions']),
            Conditions=self.__ArrayToString(j['conditions']),
            Limitations=self.__ArrayToString(j['limitations']),
            Body=j['body']
        )

    def __GetHttpHeaders(self):
        return {
            "Accept": "application/vnd.github.drax-preview+json",
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token())
        }

    def __ReturnResponse(self, r, success_code=None, sleep_time=2, is_show=True):
        if is_show:
            print("HTTP Status Code: {0}".format(r.status_code))
            print(r.text)
        time.sleep(sleep_time)
        if None is not success_code:
            if (success_code != r.status_code):
                raise Exception('HTTP Error: {0}'.format(r.status_code))
                return None
        return json.loads(r.text)

    def __BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0

    def __ArrayToString(self, array):
        ret = ""
        for v in array:
            ret = v + ','
        return ret[:-1]
