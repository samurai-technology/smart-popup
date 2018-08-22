#!/usr/bin/env bash
docker run -v mongo-data:/data/db -d -p 27017:27017 --net smart-popup-network --name smart-popup-mongo mongo