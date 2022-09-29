#!/bin/bash
## Use this script to stop the flask API

image_tag="flask_api:1"
containers=$(docker ps -a -q --filter ancestor=$image_tag --format="{{.ID}}")
if [ -z "$containers" ]; then
    echo "No containers running"
else
    echo "Stopping containers with tag $image_tag..."
    docker stop $containers
    docker rm $containers
fi