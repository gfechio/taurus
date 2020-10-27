#!/bin/bash

docker login --username=$USERNAME 

docker build -t $USERNAME/taurus:api api/
docker push $USERNAME/taurus:api
docker build -t $USERNAME/taurus:processor processor/
docker push $USERNAME/taurus:processor
docker build -t $USERNAME/taurus:puller puller/
docker push $USERNAME/taurus:puller
