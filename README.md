# Social Networking Application API

This Django project implements a RESTful API for a social networking application using Django Rest Framework (DRF). It includes user authentication, user search, friend request handling, and other functionalities typical of a social network.


## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/prudhvikollanapK/SocialNetwork.git
    cd social_network
    ```

2. **Set up the virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create the superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7.**Open this url in browser**
  ```bash
  http://127.0.0.1:5000
  ```

## API Documentation
**Postman Collection :**

Import the provided Postman collection (Social Network API.postman_collection.json) into your Postman application. 
The collection includes examples of various API endpoints:

- User Signup
- User Login
- User Search
- Send Friend Request
- Accept Friend Request
- Reject Friend Request
- List Friends
- List Pending Friend Requests

