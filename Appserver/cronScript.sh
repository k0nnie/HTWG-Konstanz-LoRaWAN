!/bin/sh
if  ps -ef | grep -v grep | grep receiver.py ; then
    exit 0
else
    /usr/bin/python3 receiver.py
    exit 0
fi
