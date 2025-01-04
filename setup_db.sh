#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Start MongoDB container
echo "Starting MongoDB container..."
sudo docker run -dp 27017:27017 -v local-mongo:/data/db --name local-mongo --restart=always mongo:latest

# Wait for MongoDB to start
echo "Waiting for MongoDB to start..."
sleep 10

# Check if MongoDB container is running
if ! sudo docker ps | grep -q local-mongo
then
    echo "MongoDB container is not running. Please check Docker and try again."
    exit 1
fi

# Open MongoDB port in UFW
echo "Opening port 27017 in UFW..."
sudo ufw allow 27017

# Create database and collections
echo "Configuring MongoDB database for CDMS..."
# Using docker exec to run MongoDB shell commands
sudo docker exec -i local-mongo mongo <<EOF
use cdms
db.createCollection("cards")
db.createCollection("library")
db.createCollection("trade")
db.createCollection("sell")
EOF

echo "MongoDB setup is complete."
echo "To connect to the MongoDB shell, use the following command:"
echo "sudo docker exec -it local-mongo mongo"
