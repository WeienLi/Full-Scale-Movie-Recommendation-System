#!/bin/bash
## Use this script to start the flask API in a docker container (background)

image_tag="flask_api:1"
if [ "$(docker images -q $image_tag 2> /dev/null)" != "" ]; then
    ./stop.sh
    echo "Removing the existing container..."
    docker rmi $image_tag -f
fi
echo "Building the image..."
docker build -t "$image_tag" .
echo "Starting the container..."
docker run -d -p 8082:8082 "$image_tag"