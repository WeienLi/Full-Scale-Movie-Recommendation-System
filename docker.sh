#!/bin/bash
## Use this script to start/stop the project in a Docker container

cmd=$1
flask_api_tag="flask_api"

# Stop all existing Docker containers
function stop() {
    containers=$(docker ps -a -q)
    if [ -z "$containers" ]; then
        echo "No containers running"
    else
        echo "Stopping containers..."
        docker stop $containers
    fi
}

# Create and start all Docker images and containers
function start() {
    containers=$(docker ps -a -q)
    if [ -n "$containers" ]; then
        flask_api_container=$(docker ps -a | grep $flask_api_tag | awk '{print $1}')
        # remove flask_api container if it exists
        if [ -n "$flask_api_container" ]; then
            docker stop $flask_api_container
            docker rm $flask_api_container
        fi
        flask_api_image=$(docker images | grep $flask_api_tag | awk '{print $3}')
        # remove flask_api image if it exists
        if [ -n "$flask_api_image" ]; then
            docker rmi $flask_api_image
        fi
        stop
    fi

    echo "Starting new containers..."
    docker-compose up -d
}

# remove all Docker containers, images, and volumes
function reset() {
    # remove all containers if they exist
    containers=$(docker ps -a -q)
    if [ -n "$containers" ]; then
        stop
        docker rm $containers
    fi
    # remove all images if they exist
    images=$(docker images -q)
    if [ -n "$images" ]; then
        docker rmi $images
    fi
    # remove all volumes if they exist
    volumes=$(docker volume ls -q)
    if [ -n "$volumes" ]; then
        docker volume rm $volumes
    fi
    echo "All containers, images, and volumes removed"
}

if [ "$cmd" == "start" ]; then
    start
elif [ "$cmd" == "stop" ]; then
    stop
elif [ "$cmd" == "reset" ]; then
    reset
else
    echo "Usage: docker.sh [start|stop|reset]"
fi
