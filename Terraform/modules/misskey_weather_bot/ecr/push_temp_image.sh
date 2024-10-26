#!/bin/bash

aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
docker pull hello-world:latest
docker tag hello-world:latest ${REPOSITORY_URL}:temp
docker push ${REPOSITORY_URL}:temp
