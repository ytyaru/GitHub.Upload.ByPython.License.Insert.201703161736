#!python3
#encoding:utf-8
import sys
import getpass
import Main
github_user_name = sys.argv[1]
description = sys.argv[2]
homepage = sys.argv[3]
path_dir_pj = sys.argv[4]

# Accounts, RepositoriesのDBパスを生成する。
# 自分の環境にあわせてパスを生成すること。
os_user_name = getpass.getuser()
device_name = 'some_device_name'
path_db_base = 'some_dir/db/GitHub'
path_db_account = '/media/{0}/{1}/{2}/private/v0/GitHub.Accounts.sqlite3'.format(os_user_name, device_name, path_db_base)
path_db_repo = '/media/{0}/{1}/{2}/public/v0/GitHub.Repositories.{3}.sqlite3'.format(os_user_name, device_name, path_db_base, github_user_name)
path_db_license = '/media/{0}/{1}/{2}/public/v0/GitHub.Licenses.sqlite3'.format(os_user_name, device_name, path_db_base)

main = Main.Main(github_user_name, description, homepage, path_dir_pj, path_db_account, path_db_repo, path_db_license)
main.Run()

