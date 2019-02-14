PID=$(pgrep -f receiver.py)
kill -9 $PID
PID=$(pgrep -f api_server.py)
kill -9 $PID
