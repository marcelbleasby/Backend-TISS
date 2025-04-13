#!/bin/bash

# Check if the database container is already running
if [ "$(docker ps -q -f name=tiss_db)" ]; then
    echo "Database container is already running."
else
    # Start the database container
    echo "Starting database container..."
    docker-compose up -d db
    
    # Wait for the database to be ready
    echo "Waiting for database to be ready..."
    sleep 5
    
    echo "Database is ready!"
fi 