# Habit-Tracker

This is a REST API habit tracker built with Django Rest Framework (DRF).

## Features

- User registration and authentication
- Habit creation and management
- Periodic notifications for habits
- Integration with Telegram for notifications

The project is currently located on the server and is being deployed using Docker and GitHub Actions.
IP-address id following: http://ec2-16-171-154-166.eu-north-1.compute.amazonaws.com/

# Instructions for deploy on the server

## Prepare a remote server

1. **Create a remote server**: You can use any cloud provider (e.g., AWS, DigitalOcean, etc.) to create a remote server.
2. **Fill up info**:
      - Create .env file inside the project directory and fill up it according to .env.sample
      - Add necessary secrets and variables in the GitHub actions secrets section.

### Here is the overview of necessary secrets inside GitHub actions:
- 'DJANGO_SECRET_KEY' - Django secret key for the project.
- 'DOCKER_USERNAME' - Docker Hub username.
- 'DOCKER_PASSWORD' - Docker Hub password.
- 'SERVER_IP' - IP address of the remote server.
- 'SSH_KEY' - SSH key for accessing the remote server.
- 'SSH_USER' - SSH user for accessing the remote server.
- 'POSTGRES_USER' - PostgreSQL username.
- 'POSTGRES_PASSWORD' - PostgreSQL password.

### Overview of necessary variables inside GitHub actions:
- 'CELERY_BROKER_URL' - URL for the Celery broker (Redis). **Default example: redis://redis:6379/1**
- 'CELERY_RESULT_BACKEND' - URL for the Celery result backend (Redis). **Default example: redis://redis:6379/1**
- 'REDIS_HOST' - Redis host. **Default example: redis://redis:6379//**
- 'DEBUG' - Debug mode for Django. **Default example: True**
- 'POSTGRES_DB' - PostgreSQL database name. **First create database locally on your machine**
- 'POSTGRES_HOST' - PostgreSQL host. **Default example: db - as specified inside docker-compose.yml (service: db)**
- 'POSTGRES_PORT' - PostgreSQL port. **Default example: 5432**

## Once you have set up the remote server and filled in the necessary secrets and variables, you can proceed with the installation of necessary dependencies.

1. **Connect to your server via SSH** (check your server provider's documentation for details):
    ```sh
    ssh <username>@<server_ip>
    ```
2. **Firewall setup**:
   Run following commands to set up the firewall:
    ```sh    
   sudo ufw --force enable
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 5432/tcp
   sudo ufw allow 6379/tcp
   sudo ufw allow 8000/tcp
   sudo ufw allow 587/tcp
   ```
3. **Install Docker and Docker Compose**:
   Execute the following commands or follow the official Docker installation guide for your OS:
   ```sh 
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc
   
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update -y
   sudo apt-get upgrade -y
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   sudo apt-get update
   ```

4. **Install Git**:
   ```sh
   sudo apt-get install -y git
   sudo git --version
   ```
5. **Clone the repository and cd to project directory**:
   ```sh
    git clone <repository_url>
    cd <repository_directory>
    checkout <branch_name> # if necessary
    ```
6. **Create and configure the `.env` file**:
   ```sh
   cp .env.sample .env
   # Edit the .env file to set your environment variables using nano or vim
   ```

GitHub Actions will automatically build the Docker image, push it to Docker Hub, and deploy it to the remote server.
You just have to proceed with push or pull request and if all set up correctly, the deployment will be done automatically.

If you want to create a new admin user, you can do it by running the following command on the remote server:
#### Note: First cd to the project directory.
#### Note: If you are facing permission issues, you can use sudo command.

```sh
docker exec backend python3 manage.py createadmin
```

Now you can access to your remote server using the IP address. For more detailed information about project structure, please continue to follow the guide
 
# Project Local Setup Instructions

First of all, make sure you have Docker and Docker Compose installed on your machine.

## Running the Project with Docker Compose

Follow these steps to run the project using `docker-compose`:

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
   git checkout <branch_name> # if necessary
    ```

2. **Create and configure the `.env` file**:
    ```sh
    cp .env.sample .env
    # Edit the .env file to set your environment variables
    ```

3. **Build and start the Docker containers**:
    ```sh
    docker-compose up --build
    ```
   ### Note: Make sure you have created a database locally on your machine

## Starting the Project

To start the project on the background from scratch, use the following command:
```sh
docker-compose up -d --build
```

This command will build and start all the services defined in the `docker-compose.yml` file.

## Verifying Service Functionality

After starting the project, you can verify that all services are running correctly. The following commands will help you set up the initial data and test users:

- Create a superuser for the Django admin:
    ```sh
    docker-compose exec backend python manage.py createadmin
    ```
  login: admin@test.com
  password: adminpass
 

## Usage

### Register a New User

To register a new user, send a POST request to `/register/` with the following data:
```json
{
    "email": "newuser@example.com",
    "password": "newpassword123"
}
```

### Update User Profile
To update the user profile, including adding your Telegram ID, send a PATCH request to */users/<user_id>/update/* with the following data:
```json
{
    "tg_chat_id": "your_telegram_chat_id"
}
```

### Retrieve Telegram Chat ID
To retrieve the Telegram chat ID for the authenticated user, send a GET request to /chat_id/.


### Telegram Integration
To receive notifications via Telegram, you need to add your Telegram chat ID to your user profile. Follow these steps:


1. Start a chat with your Telegram bot and send any message.
2. The bot will receive the message and you can retrieve your chat ID.
3. Update your user profile with the retrieved chat ID as shown in the "Update User Profile" section.

### Running Celery
To run the Celery worker, use the following command:
```sh
celery -A config worker --loglevel=info 
```

If you using windows, you can run the Celery worker with the following command:
```sh
celery -A config worker -l INFO -P eventlet
```

To run Celery beat, use the following command:
```sh
celery -A config beat -l INFO
```

### Running Tests
To run the tests, use the following command:
```sh
python manage.py test
```

### Check coverage
To check test coverage, use the following command:
```sh
coverage report
```