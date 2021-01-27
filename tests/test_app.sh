#!/bin/bash

echo "Starting application in the background."
python app.py &
sleep 3
PID=`ps -ef | grep app.py | head -1 | awk '{ print $2 }'`
echo "The PID of the application is $PID"

echo "Starting tests."
python tests/test_app.py
EXIT_CODE=$?
echo "Finished with testing."
echo "The exit code of the tests was: $EXIT_CODE"

echo "Stopping the application"
kill $PID

exit $EXIT_CODE
