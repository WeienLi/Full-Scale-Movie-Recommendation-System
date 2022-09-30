#!/bin/bash
## Use this script to start/stop the project in a Docker container

cmd=$1
image_tag="flask_api:1"

# Stop the flask API and remove any pre-existing Docker containers
function stop() {
    containers=$(docker ps -a -q --filter ancestor=$image_tag --format="{{.ID}}")
    if [ -z "$containers" ]; then
        echo "No containers running"
    else
        echo "Stopping containers with tag $image_tag..."
        docker stop $containers
        docker rm $containers
    fi
}

# Start the flask API in a Docker container (background)
function start() {
    if [ "$(docker images -q $image_tag 2> /dev/null)" != "" ]; then
        stop
        echo "Removing the existing container..."
        docker rmi $image_tag -f
    fi
    echo "Building the image..."
    docker build -t "$image_tag" .
    echo "Starting the container..."
    docker run -d -p 8082:8082 "$image_tag"
}

if [ "$cmd" == "start" ]; then
    start
elif [ "$cmd" == "stop" ]; then
    stop
else
    echo "Invalid command"
fi
