#!/bin/bash
docker build -t taurus:api app/api/
docker build -t taurus:worker app/worker/
docker build -t taurus:searcher app/searcher/
