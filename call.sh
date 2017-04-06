#!/bin/bash
user_name=ytyaru
description=説明文。
homepage=http://abc
path_dir_pj=$(cd $(dirname $0) && pwd)

path_script=/some_script_dir/up.py
python3 ${path_script} ${user_name} ${description} ${homepage} ${path_dir_pj}

