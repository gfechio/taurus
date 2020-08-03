#!/bin/bash
docker build -t $USERNAME/taurus:api app/api/ --push
docker build -t $USERNAME/taurus:worker app/worker/ --push
docker build -t $USERNAME/taurus:searcher app/searcher/ --push
