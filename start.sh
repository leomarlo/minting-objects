#! /bin/bash

# if the argument provided is --local, then start the docker-compose-only-db.yml file, if the argument provided is --development, then start the docker compose with the docker-compose.yml file, if the argument provided is --production, then start the docker compose with the docker-compose-production.yml

if [ "$1" == "--local" ]; then
    echo "--> Starting local development environment"
    docker-compose -f docker-compose-only-db.yml up -d
    sleep 3
    ## start backend
    echo "--> Starting backend flask server"
    source .env
    cd backend
    export FLASK_ENV=local
    export REACT_APP_DEVELOPMENT_MODE=local
    # Combine the path with the file
    export GOOGLE_CREDENTIAL_PATH="/home/leonhard/Projects/Hallein/minting-objects-game/backend/env/$GOOGLE_CREDENTIAL_FILE"
    echo $GOOGLE_CREDENTIAL_PATH
    # Activate the virtual environment
    .venv/bin/python app.py &
    sleep 3
    ## start frontend
    echo "--> Starting frontend react server"
    cd ../frontend
    # yarn start:dev-open 
    yarn install
    yarn start:next:dev:port 
    # done  
    cd ..
    echo "--> Done"
elif [ "$1" == "--development" ]; then
    ## if the second argument is --build then echo hello, else say hi
    if [ "$2" == "--build" ]; then
        echo "--> Starting development environment with build"
        docker-compose up --build
    else
        echo "--> Starting development environment without build"
        docker-compose up
    fi
    echo "--> Done"
elif [ "$1" == "--production" ]; then
    echo "--> Starting production environment"
    docker-compose -f docker-compose-production.yml up -d
    echo "--> Done"
else
    echo "Please provide an argument: --local, --development or --production"
fi

