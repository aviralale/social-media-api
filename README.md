# Django Social Media Application

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [WebSocket Endpoints](#websocket-endpoints)

## Introduction
This is a social media application built with Django. It includes features for managing notifications, posts, comments, replies, media, followers, and chat functionalities.

## Features
- User authentication and profiles
- Post creation, commenting, and liking
- Follower and following system
- Real-time chat with WebSocket support
- Notifications system

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/aviralale/social-media-api.git
    cd social-media-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Running the Project
After setting up the project, you can run the development server with the following command:
```sh
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/admin` to access the admin interface and manage your data.

## API Endpoints
Here are the main API endpoints provided by the application:

### Account Endpoints
- **Authentication**: 
  - `POST /api/auth/jwt/create/` - Create JWT tokens
  - `POST /api/auth/jwt/refresh/` - Refresh JWT tokens
  - `POST /api/auth/jwt/verify/` - Verify JWT tokens
  - `GET /api/auth/users/me/` - Get current user details
- **User Profile**: 
  - `GET /api/user/<str:username>/` - Get user profile details

### Social Endpoints
- **Posts**: 
  - `GET /api/posts/` - List all posts
  - `POST /api/posts/` - Create a new post
  - `GET /api/posts/<int:pk>/` - Retrieve a post
  - `POST /api/posts/<int:pk>/like/` - Like a post
  - `GET /api/posts/<int:pk>/comments/` - List comments on a post
  - `GET /api/posts/<int:pk>/likers/` - List users who liked a post

- **Comments**: 
  - `GET /api/comments/` - List all comments
  - `POST /api/comments/` - Create a new comment
  - `GET /api/comments/<int:pk>/` - Retrieve a comment
  - `POST /api/comments/<int:pk>/like/` - Like a comment
  - `GET /api/comments/<int:pk>/replies/` - List replies to a comment
  - `GET /api/comments/<int:pk>/likers/` - List users who liked a comment

- **Replies**: 
  - `GET /api/replies/` - List all replies
  - `POST /api/replies/` - Create a new reply
  - `GET /api/replies/<int:pk>/` - Retrieve a reply
  - `POST /api/replies/<int:pk>/like/` - Like a reply
  - `GET /api/replies/<int:pk>/likers/` - List users who liked a reply

- **Followers**: 
  - `GET /api/followers/` - List all followers
  - `POST /api/followers/follow/` - Follow a user
  - `DELETE /api/followers/<str:username>/unfollow/` - Unfollow a user

- **User-specific**: 
  - `GET /api/users/<str:username>/posts/` - List posts by user
  - `GET /api/users/<str:username>/posts/<int:pk>/` - Retrieve a specific post by user
  - `GET /api/users/<str:username>/followers/` - List followers of user
  - `GET /api/users/<str:username>/following/` - List users followed by user
  - `GET /api/users/<str:username>/mutual-connections/` - List mutual connections

### Chat Endpoints
- **Chat**: 
  - `GET /api/chats/` - List user chats
  - `POST /api/start/<str:username>/` - Start chat with user
  - `GET /api/room/<int:room_id>/` - Get chat room details
  - `POST /api/room/<int:room_id>/typing/` - Update typing status in chat room

### Notifications Endpoints
- **Notifications**: 
  - `GET /api/notifications/` - List all notifications
  - `GET /api/notifications/<int:pk>/` - Retrieve a notification
  - `POST /api/notifications/mark-all-as-read/` - Mark all notifications as read

## WebSocket Endpoints
- **Chat**: 
  - `ws/chat/<room_id>/` - WebSocket endpoint for chat room

- **Notifications**: 
  - `ws/notifications/` - WebSocket endpoint for notifications
