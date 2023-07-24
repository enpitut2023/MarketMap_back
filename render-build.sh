#!/usr/bin/env bash
# exit on error
set -o errexit

wget -P ~/.fonts https://github.com/evosystem-jp/heroku-buildpack-cjk-font/raw/master/fonts/wqy-microhei.ttc
wget -P ~/.fonts https://github.com/evosystem-jp/heroku-buildpack-cjk-font/raw/master/fonts/wqy-zenhei.ttc