!/bin/sh
if  ps -ef | grep -v grep | grep api_server.py ; then
    exit 0
else
    /usr/bin/python3 api_server.py
    exit 0
fi
