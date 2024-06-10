# Article-django
## Overview
This project is a Django-based web application designed to manage articles and their associated points. The application uses Docker for containerization, pre-commit for code quality checks, and GitHub Actions for continuous integration.

## Get Started
Before you can run this project, you need to have the following installed:
- Docker
- Docker Compose

## Running the Project with Docker
Use Docker Compose to build and start the containers:
```bash
docker-compose up --build -d
```
### Create a Superuser
To access the Django admin interface, you need to create a superuser:
```bash
docker-compose exec app_article python manage.py createsuperuser
```

### Access the Application
The application should now be running and accessible at http://localhost:8000.
API Documentation (using Spectacular): http://localhost:8000


## Development

### Software Optimal & Secure Flow:
We have total_points and average_points to store final points.
New data is cached for 30 minutes.
If points exceed 100, point creation is disabled to prevent abuse.


### Use Pre-commit for development
At first install pre-commit package:
```bash
pip install pre-commit
```

Then install pre-commit on your desktop:
```bash
pre-commit install
```

Then you can use it with ```git commit``` and it will automatically check your files before committing.

### TODO: list of requirements of project:
- [x] Initialize Django Project
- [x] Dockerize Project
- [x] Clean code checker with pre-commit
- [x] Github action for code check and tests
- [x] Start Article app
    - [x] Model Creation
    - [x] Initialize Django REST API
    - [x] Initialize Spectacular REST API for documentation
    - [x] Implement ListView for Article
    - [x] Implement Point Creation
    - [x] Add points to Article
- [x] Security & Optimal Software Design
    - [x] Optimal Plan & Flowchart
    - [x] Security Plan for Flood points
    - [x] Optimize Model
    - [x] Optimize Viewsets
    - [x] Optimize Application
- [ ] Tests
    - [ ] Create sample data
    - [x] Test Model
    - [x] Test Api
    - [ ] Test Large datasets
- [ ] Finalize Project
    - [x] Documentation
        - [x] Documentation of deployment
        - [x] Documentation of software
        - [x] Screenshots
    - [ ] Change Private Repository to Public
