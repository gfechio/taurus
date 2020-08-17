#!/bin/bash
docker build --platform linux/arm/v7 -t $USERNAME/taurus:api app/api/ 
docker push $USERNAME/taurus:api
docker build --platform linux/arm/v7 -t $USERNAME/taurus:worker app/worker/ 
docker push $USERNAME/taurus:worker
docker build --platform linux/arm/v7 -t $USERNAME/taurus:searcher app/searcher/ 
docker push $USERNAME/taurus:searcher
