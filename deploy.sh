#!/usr/bin/env sh

docker build -f .deploy/Dockerfile -t securtest .

docker stop securtest || true
docker rm securtest || true



docker run -d -p 0.0.0.0:80:80 --name securtest securtest:latest
