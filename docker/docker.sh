#!/bin/bash

print_help() {
   echo "Wrapper under docker API for world_creator.
It encapsulates all necessary docker flags and properly handles image versions.
https://github.com/PonomarevDA/world_creator

usage: docker.sh [command]

Commands:
build                           Build docker image.
interactive                     Run container in interactive mode.
kill                            Kill all containers.
help                            Print this message and exit"
}

DOCKERFILE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_DIR=$DOCKERFILE_DIR/..

setup_image_name_and_version() {
    TAG_NAME=v0.1.0
    DOCKERHUB_REPOSITOTY=ponomarevda/world_creator

    if uname -m | grep -q 'aarch64'; then
        TAG_NAME="$TAG_NAME""arm64"
    elif uname -m | grep -q 'x86_64'; then
        TAG_NAME="$TAG_NAME""amd64"
    else
        echo "unknown architecture"
        exit
    fi
    DOCKER_CONTAINER_NAME=$DOCKERHUB_REPOSITOTY:$TAG_NAME
}

build_docker_image() {
    setup_image_name_and_version
    docker build -f $DOCKERFILE_DIR/Dockerfile -t $DOCKER_CONTAINER_NAME ..
}

run_interactive() {
    setup_image_name_and_version
    docker container run --rm -it $DOCKER_FLAGS $DOCKER_CONTAINER_NAME /bin/bash
}

kill_all_containers() {
    docker kill $(docker ps -q)
}

cd "$(dirname "$0")"

if [ \( "$1" = "build" \) -o \( "$1" = "b" \) ]; then
    build_docker_image
elif [ \( "$1" = "interactive" \) -o \( "$1" = "i" \) ]; then
    run_interactive
elif [ "$1" = "kill" ]; then
    kill_all_containers
else
    print_help
fi
