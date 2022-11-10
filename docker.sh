#!/bin/bash
## Use this script to start/stop the project in a Docker container

cmd=$1
flask_api_tag="flask_api"
project_images=( $flask_api_tag "prometheus" "grafana" "alertmanager" "redis" "kafka-consumer" "redis-exporter" "traefik" )

# Stop all existing Docker containers
function stop() {
    echo "Stopping project containers..."
    for image in "${project_images[@]}"; do
        container=$(docker ps -a | grep $image | awk '{print $1}')
        if [ -n "$container" ]; then
            docker stop $container
        fi
    done
}

# Create and start all Docker images and containers
function start() {
    export GITHUB_SHA=$(git rev-parse --short HEAD)
    echo "Starting containers..."
    docker-compose up -d --build
}

# remove all Docker containers, images, and volumes associated with the project
function reset() {
    for image in "${project_images[@]}"; do
        # remove project containers
        container=$(docker ps -a | grep $image | awk '{print $1}')
        if [ -n "$container" ]; then
            docker stop $container
            docker rm $container
        fi
        # remove project images
        image=$(docker images | grep $image | awk '{print $3}')
        if [ -n "$image" ]; then
            docker rmi $image
        fi
        # remove all dangling volumes
        volumes=$(docker volume ls -qf dangling=true)
        if [ -n "$volumes" ]; then
            docker volume rm $volumes
        fi
    done
    echo "All associated containers, images, and volumes removed"
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
