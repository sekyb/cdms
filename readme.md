# CDMS (Card Database Management System) Documentation

## Overview

CDMS (Card Database Management System) is a command-line tool to manage your Magic: The Gathering card collection. You can add, view, search, and delete cards in your database, with integration to Scryfall for fetching card details.

This document outlines how to use CDMS and how to set up the necessary environment using Docker.

## Prerequisites

- **Python 3.x**: Ensure Python 3.x is installed on your system.
- **MongoDB**: CDMS uses MongoDB as its database.
- **Docker**: Required for containerizing MongoDB.

## Installation

### Setting Up MongoDB with Docker

1. **Create the Docker Setup Script**

Save the following as `setup-mongodb.sh`:

```bash
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
```

# Make the Script Executable
chmod +x setup-mongodb.sh

./setup-mongodb.sh

This script will start a MongoDB container, configure it for CDMS, and open the necessary port.

# Using CDMS
---
## Add or Update a Card
python CDMS.py add-card --id <collection_id> --n "<card_name>" --quantity <quantity> [--foil] [--extended_art] [--etched] [--location "<location>"]

--id: The ID of the collection.
--n: The name of the card.
--quantity: The quantity of the card.
--foil: (Optional) Indicates if the card is foil.
--extended_art: (Optional) Indicates if the card has extended art.
--etched: (Optional) Indicates if the card is etched.
--location: (Optional) Location of the card (default is "Trades").
Example:
python CDMS.py add-card --id 1 --n "Black Lotus" --quantity 1 --foil --location "Rares"

## View All Cards
python CDMS.py view-db
This command displays all cards in the database.

##Search for a Card in the Local Database
python CDMS.py search-local --n "<card_name>"
Example:
python CDMS.py search-local --n "Black Lotus"

##Search for a Card on Scryfall
python CDMS.py search-scryfall --n "<card_name>"
Example:
python CDMS.py search-scryfall --n "Black Lotus"

##Delete a Card
python CDMS.py delete-card --n "<card_name>"
Example:
python CDMS.py delete-card --n "Black Lotus"

#Command-Line Help
To view help for each command, use the -h flag:
Example:
python CDMS.py <command> -h
Replace <command> with one of the commands (add-card, view-db, search-local, search-scryfall, delete-card).

##Docker Script Explanation
Check for Docker: Ensures Docker is installed on your system.
Start MongoDB Container: Runs MongoDB in a Docker container and maps the container port to the host.
Wait for MongoDB to Start: Gives MongoDB some time to initialize.
Check MongoDB Status: Verifies that MongoDB is running.
Open Port in UFW: Opens the MongoDB port in the firewall (UFW).
Create Database and Collections: Configures MongoDB by creating the necessary database and collections for CDMS.
---
##Troubleshooting
MongoDB Not Running: Ensure Docker is running and check Docker logs using sudo docker logs local-mongo.
Script Errors: Verify that Docker and UFW commands are correct and that Docker is properly installed.
This document should guide you through setting up and using CDMS. If you encounter any issues, consult the relevant logs or documentation for Docker and MongoDB.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Developed by [sekyb](https://github.com/sekyb)**
