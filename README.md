# Article-django



## Development

### Software Optimal & Secure Flow:
We have a total_points & average_points to store final points.
Save New data into cache for 30 minutes if points more than 100 we disable points creation.


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
    - [ ] Test Model
    - [ ] Test Api
    - [ ] Test Large datasets
- [ ] Finalize Project
    - [ ] Documentation
        - [ ] Documentation of deployment
        - [ ] Documentation of software
        - [ ] Screenshots
    - [ ] Change Private Repository to Public
