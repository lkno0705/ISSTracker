#!/bin/sh
apt-get update
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install redis -y

pip3 install requests
pip3 install redis
pip3 install feedparser
pip3 install pytz
