# このソフトウェアについて

GitHubリポジトリ作成スクリプトにライセンス取得機能を追加した。

[前回](GitHub.Upload.ByPython.Refactoring.201703101718)の改良版。

* `AddCommitPush()`したらライセンス情報を取得しDBに挿入する
* 削除するときライセンス情報も対象にした

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [Python 3.4.4](https://www.python.org/downloads/release/python-344/)
    * [requests](http://requests-docs-ja.readthedocs.io/en/latest/)
    * [dataset](https://github.com/pudo/dataset)

## WebService

* [GitHub](https://github.com/)
    * [アカウント](https://github.com/join?source=header-home)
    * [AccessToken](https://github.com/settings/tokens)
    * [Two-Factor認証](https://github.com/settings/two_factor_authentication/intro)
    * [API v3](https://developer.github.com/v3/)

# 準備

## 必要なデータベースを作成する

* [GitHub.Accounts.Database](https://github.com/ytyaru/GitHub.Accounts.Database.20170107081237765)
    * [GiHubApi.Authorizations.Create](https://github.com/ytyaru/GiHubApi.Authorizations.Create.20170113141429500)
* [GitHub.Licenses.Database.Create.201703140852](GitHub.Licenses.Database.Create.201703140852)
    * [GitHub.Licenses.Database.Insert.201703141133](https://github.com/ytyaru/GitHub.Licenses.Database.Insert.201703141133)
    * [GitHub.Licenses.Database.Insert.Pagenation.201703142055](https://github.com/ytyaru/GitHub.Licenses.Database.Insert.Pagenation.201703142055)
* [GitHub.Repositories.Database.Create.20170114123411296](https://github.com/ytyaru/GitHub.Repositories.Database.Create.20170114123411296)
    * [GitHub.Repository.Licenses.Database.Create.201703140912](https://github.com/ytyaru/GitHub.Repository.Licenses.Database.Create.201703140912)
    * [GitHub.Repository.Licenses.Database.Insert.201703141352](https://github.com/ytyaru/GitHub.Repository.Licenses.Database.Insert.201703141352)

# 実行

## 1. 起動する

1. ターミナルを起動する
1. 以下のコマンドを実行する（今回のスクリプトを実行する）

```sh
bash call.sh
```

# ライセンス #

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

