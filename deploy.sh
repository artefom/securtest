#!/usr/bin/env sh

docker build -f .deploy/Dockerfile -t securtest .

docker stop securtest || true
docker rm securtest || true

docker run -d -p 80:80 -p 443:443 --name securtest securtest

