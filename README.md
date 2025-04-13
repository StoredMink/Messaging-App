# DevOps Message System

A simple DevOps practice project demonstrating Docker, Nginx, Redis, Python, and MySQL integration.
WARNING: Due to its simplicity, the application lacks some sequerity, like Redis paasword. Please do sequerity audit before using this project in prod enviroment.

![Examples of usage](Messaging-App/Screenshot 2025-04-10 235202.png)

## Project Overview

This project implements a simple message queue system with the following components:

- **Frontend**: A single-page website with a button that allows users to enter messages
- **Queue**: Redis for temporary storage of messages
- **Backend**: Python service that processes messages from Redis and stores them in a database
- **Database**: MySQL for permanent storage of messages with timestamps
- **Orchestration**: Docker Compose for managing all containers

## Architecture

```
User -> Nginx -> Python Backend -> Redis -> Python Worker -> MySQL
```

1. User submits a message through the web interface
2. Nginx forwards the request to the Python backend
3. Python adds the message to Redis queue
4. A worker process retrieves messages from Redis
5. The worker stores messages in the MySQL database

## Prerequisites

- Docker and Docker Compose
- Git (optional)

## Project Structure

```
project/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── html/
│       ├── index.html
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── redis/
│   └── redis.conf
└── db/
    └── init.sql
```

## Setup Instructions

### 1. Clone or Create the Project

```bash
# Create directories
mkdir -p devops-message-system/frontend/html devops-message-system/backend devops-message-system/redis devops-message-system/db
cd devops-message-system
```

### 2. Create Configuration Files

#### Frontend Files

**frontend/html/index.html**: The main user interface
**frontend/nginx.conf**: Nginx configuration to serve the frontend and proxy API requests
**frontend/Dockerfile**: Docker configuration for the frontend

#### Backend Files

**backend/app.py**: Python application code
**backend/requirements.txt**: Python dependencies
**backend/Dockerfile**: Docker configuration for the backend

#### Redis Files

**redis/redis.conf**: Redis configuration file

#### Database Files

**db/init.sql**: SQL script to initialize the database

#### Docker Compose

**docker-compose.yml**: Configuration for all services

### 3. Build and Run

```bash
# Start all services
docker-compose up --build

# Run in background mode
docker-compose up -d --build
```

### 4. Access the Application

- Web Interface: `http://YOUR_SERVER_IP`
- Admin Interface (if added): `http://YOUR_SERVER_IP/admin.html`
- Adminer (if added): `http://YOUR_SERVER_IP:8080`

## Usage

1. Open the web interface in a browser
2. Click the "Enter a Message" button
3. Type a message and click "Send"
4. The message will be processed through Redis and stored in the database

## Checking the Database

### Option 1: Command Line

```bash
# Connect to the MySQL container
docker-compose exec db mysql -u user -ppassword messages_db

# View messages
SELECT * FROM messages;
```

### Option 2: Using Adminer

1. Access Adminer at `http://YOUR_SERVER_IP:8080`
2. Log in with:
   - System: MySQL
   - Server: db
   - Username: user
   - Password: password
   - Database: messages_db

## Troubleshooting

### Redis Connection Issues

If you encounter Redis connection errors, try these steps:

```bash
# Check Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis

# Force rebuild all containers
docker-compose down
docker-compose up --build
```

### Database Connection Issues

```bash
# Check database logs
docker-compose logs db

# Verify database is running
docker-compose ps db
```

## Management Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs

# View logs for a specific service
docker-compose logs backend

# Restart a specific service
docker-compose restart backend

# SSH into a container
docker-compose exec backend sh
```
