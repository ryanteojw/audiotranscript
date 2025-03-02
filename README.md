# Audio Transcript Website

## Prerequisites
Ensure you have the following installed on your system:
- Docker

## Frontend Vue.js Application
### Build the Docker image:
docker-compose -f frontend/docker-compose.yaml build

### Running the Application with Docker:
docker-compose -f frontend/docker-compose.yaml up

### Running unit tests:
1) Change to the frontend directory
2) Run this command "npm run test:unit"

## Backend Flask Application
### Build the Docker image:
docker-compose -f backend/docker-compose.yaml build

### Running the Application with Docker:
docker-compose -f backend/docker-compose.yaml up

### Running unit tests:
1) Change to the backend directory
2) Run this command "python -m unittest discover tests"
