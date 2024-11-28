# To-Do List Application (Backend)

This is a backend implementation of a simple To-Do List application using Django, Django REST Framework (DRF), and other related tools. The project includes various features such as creating, reading, updating, and deleting tasks, along with user authentication, testing, and deployment configurations.

## Features

- **Task Management**: Allows users to create, update, delete, and view tasks.
- **Tagging**: Multiple tags can be added to tasks.
- **Status**: Tasks can have different statuses such as OPEN, WORKING, PENDING REVIEW, COMPLETED, OVERDUE, and CANCELLED.
- **Due Date**: Each task can have an optional due date.
- **Django Admin**: The app provides an admin interface for managing tasks and tags.
- **Basic Authentication**: Basic authentication is enabled for the APIs.
- **Testing**: Includes unit tests, integration tests, and end-to-end (E2E) tests for the entire system.

## Project Setup

### Prerequisites

Make sure you have the following installed on your local machine:

- Python 3.11+
- pip (Python package installer)
- PostgreSQL (if using PostgreSQL, or use SQLite by default)

### Installation Steps

1. **Clone the Repository**

   Clone this repository to your local machine.

   ```bash
   git clone https://github.com/yourusername/todo.git
   cd todo

2. **Create and Activate a Virtual Environment**

   It's recommended to create a virtual environment to isolate your project dependencies.

   On Linux/macOS:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install requirements.txt**

    ```bash
   pip install -r requirements.txt

4. **Make Migrations and Migrate**

    ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate

  if the api app tables are not created please run:
     ```bash
     python3 manage.py makemigrations api
     python3 manage.py migrate api```

5. **Create a superuser (Optional)**

    ```bash
   python3 manage.py createsuperuser

6. **Run the server**

    ```bash
   python3 manage.py runserver

7. **For Testing Run**

    ```bash
   # run all tests
   python3 manage.py test

   # run tests and generate coverage reports
   coverage run --source=api manage.py test
   coverage report
   coverage html

8. **Authentication: 
   Basic authentication is required for all API endpoints.**

***Endpoints***

**GET /api/tasks/: List all tasks**  
**POST /api/tasks/: Create a task**  
**GET /api/tasks/{id}/: Retrieve specific task**  
**PUT /api/tasks/{id}/: Update a task**  
**DELETE /api/tasks/{id}/: Delete a task**  


