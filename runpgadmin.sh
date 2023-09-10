#!/bin/bash

docker run --env-file .env --name db-client -p 8822:80 dpage/pgadmin4
docker network connect website_default db-client