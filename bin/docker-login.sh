#!/usr/bin/env bash

display_usage() {
	echo "usage: ./docker-login {ECR password} {ECR host}"
}

if [  $# -le 1 ]
then
    display_usage
    exit 1
fi
docker login -u AWS -p $1 $2
