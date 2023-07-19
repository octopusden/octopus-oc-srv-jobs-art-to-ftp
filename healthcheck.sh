#!/bin/bash

if [ -z $1 ]
then
  echo "Usage: $0 port"
  exit 1
fi

curl -X GET http://localhost:$1/ping | grep ok
