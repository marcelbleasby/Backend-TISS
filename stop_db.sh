#!/bin/bash

# Check if the database container is running
if [ "$(docker ps -q -f name=tiss_db)" ]; then
    echo "Stopping database container..."
    docker-compose stop db
    echo "Database container stopped."
else
    echo "Database container is not running."
fi 