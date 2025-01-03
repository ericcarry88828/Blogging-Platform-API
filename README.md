[![Project Page](https://img.shields.io/badge/Project%20Page-Click%20Here-brightgreen)](https://roadmap.sh/projects/blogging-platform-api)
# Blogging Platform API

![Blogging Platform API](https://assets.roadmap.sh/guest/blogging-platform-api.png)

This project implements a RESTful API with basic CRUD operations for a personal blogging platform. It is written in Python using [Flask](https://flask.palletsprojects.com/en/stable/) to provide the REST interface and and uses [flask-sqlalchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) and [pymysql](https://pymysql.readthedocs.io/en/latest/) to operate mysql

NOTE: This project does not implement a frontend client. The backend web service sends/recieves posts in JSON form. 

## Goals
The goals of this project are to:
- Demonstrate RESTful APIs and their best practices and conventions
- Demonstrate CRUD operations using an Object Relational Model (ORM)

## Features
The RESTful API allows users to perform the following operations:
- Create a new blog post
- Get a single blog post
- Get all blog posts
- Update an existing blog post
- Delete an existing blog post

## Usage
```
git clone https://github.com/ericcarry88828/Blogging-Platform-API.git
cd Blogging-Platform-API
python .\create_db.py
flask run or python run.py
```

## Install

### Pip
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
### Poetry
```
poetry install
.\.venv\Scripts\activate
```


## Environment Variables
- `.flaskenv` file is used to configure environment variables for running the Flask application in development mode.
    - `FLASK_APP`
    - `FLASK_DEBUG`

## Configure
- `instance\config.py` file is used to store sensitive or environment-specific configuration values.
    - `DEBUG`: Enable or Disable debug mode.
        - `True`: Enables debug mode (use in development only).
        - `False`: Disables debug mode (use in production).
    - `SECRET_KEY`: A secret string used for securely signing session cookies and other data.
        - Example: `"your-secret-key"`
    - `SQLALCHEMY_DATABASE_URI`: The connection string for your database.
        - Example: `mysql+pymysql://<username>:<password>@localhost:<port>/<db_name>`
    - `SQLALCHEMY_TRACK_MODIFICATIONS`: A boolean to enable/disable SQLAlchemy event notifications.
        - Recommended: False to avoid unnecessary overhead.

## Examples

### Create Blog Post
Create a new blog post using the POST method

```json
POST /posts
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

The endpoint should validate the request body and return a `201 Created` status code with the newly created blog post :

```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```
or a `400 Bad Request` status code with error messages in case of validation errors.

### Get Blog Post
Get a single blog post using the GET method

```
GET /posts/1
```
The endpoint should return a `200 OK` status code with the blog post:
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:00:00Z"
}
```
or a `404 Not Found` status code if the blog post was not found.

### Get All Blog Posts
Get all blog posts using the GET method
```
GET /posts
```
The endpoint should return a `200 OK` status code with an array of blog posts i.e.
```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "2021-09-01T12:00:00Z",
    "updatedAt": "2021-09-01T12:00:00Z"
  },
  {
    "id": 2,
    "title": "My Second Blog Post",
    "content": "This is the content of my second blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "2021-09-01T12:30:00Z",
    "updatedAt": "2021-09-01T12:30:00Z"
  }
]
```

### Update Blog Post
Update an existing blog post using the PUT method

```json
PUT /posts/1
{
  "title": "My Updated Blog Post",
  "content": "This is the updated content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

The endpoint should validate the request body and return a `200 OK` status code with the updated blog post

```json
{
  "id": 1,
  "title": "My Updated Blog Post",
  "content": "This is the updated content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2021-09-01T12:00:00Z",
  "updatedAt": "2021-09-01T12:30:00Z"
}
```

or a `400 Bad Request` status code with error messages in case of validation errors. It should return a `404 Not Found` status code if the blog post was not found.

### Delete Blog Post
Delete an existing blog post using the DELETE method
```
DELETE /posts/1
```
The endpoint should return a `204 No Content` status code if the blog post was successfully deleted or a `404 Not Found` status code if the blog post was not found.

This project idea was provided by [Roadmap](https://roadmap.sh/projects/blogging-platform-api).