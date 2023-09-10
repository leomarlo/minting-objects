#! /bin/bash

# first docker compose down

docker-compose down

export FLASK_ENV=
export GOOGLE_CREDENTIAL_PATH=
# then check if there is a process running on port 5000. If yes, kill it.

# Get the PIDs of processes running on port 5000
PIDs=$(lsof -t -i:5000)

# If processes are found, kill them
if [ -n "$PIDs" ]; then
    for PID in $PIDs; do
        kill -9 $PID
        echo "Killed backend process $PID running on port 5000."
    done
else
    echo "No backend process found running on port 5000."
fi

# then check if there is a process running on port 8086. If yes, kill it.

# Get the PIDs of processes running on port 8086
PIDs=$(lsof -t -i:8086)

# If processes are found, kill them
if [ -n "$PIDs" ]; then
    for PID in $PIDs; do
        kill -9 $PID
        echo "Killed frontend process $PID running on port 8086."
    done
else
    echo "No frontend process found running on port 8086."
fi



