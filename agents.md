# Retromanicos Backend
This is a backend created to handle most important aspects for a non-profit organization that preserves retro consoles and games. The intention is to help to handle Users (members), Material, Events
and how the material and members participate in the different events

## Stack
 -  Language: Python
 -  Framework: FastAPI
 -  Database: Mysql
 -  Test: pytest

## Commands
- `source/env/bin activate` - Start virtual environment
- `fastapi dev app/main.py` - Run project locally
- `pytest` - Run test scenarios
- `docker compose up -d` - Create docker container for the project

## Project structure

- `app/`: Main folder 
- `app/models` : All models defined
- `app/routes` : Routes defined for the different endpoints
- `app/tests` : Test scenarios for each route defined. 

## Conventions
- Use camelCase for variables and functions
- Handle errors properly, file `exception.py` contains custom exceptions for handling errors

## Important
- Don't install dependencies without authorization

## Documentation

- File `diagram E-R.png` contains E-R diagram which show tables for the database and the relationships between them.
- File `requirements.txt` contains all libraries used for the implementation