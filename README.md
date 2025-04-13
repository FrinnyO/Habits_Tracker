# Habits_Tracker

This is a REST API habit tracker built with Django Rest Framework (DRF).

## Features

- User registration and authentication
- Habit creation and management
- Periodic notifications for habits
- Integration with Telegram for notifications

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/FrinnyO/habits_tracker.git
    cd habit-tracker
    ```

2. Install Poetry if you haven't already:
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
3. To activate the Poetry environment, use the following command:
    ```sh
    poetry shell
    ```
4. Install the dependencies:
    ```sh
    poetry install
    ```
5. Apply the migrations:
    ```sh
    python manage.py migrate
    ```
6. Create an admin:
    ```sh
    python manage.py createadmin
    ```
7. Run the development server:
    ```sh
    python manage.py runserver
    ```
## Redis Requirement
This project uses Redis as the message broker for Celery. Make sure you have Redis installed and running on your system. You can start Redis with the following command:
```sh
redis-server
```
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