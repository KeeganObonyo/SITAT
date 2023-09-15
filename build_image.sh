#!/bin/bash
set -ex

ACTION=$1

checkStatus() {
  if [[ $? != 0 ]]; then
    printf "\nSomething went horribly wrong: $? \n\n"
    exit 1
  fi
}

function build {
  echo ":::::: Building SITAT ::::::"
  docker build -f callback/Dockerfile \
    -t sitat_web
}

if [[ $ACTION == 'build' ]]
then
  build
else
  echo "Invalid action"
  exit 113
fi
