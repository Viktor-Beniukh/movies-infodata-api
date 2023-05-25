# Movies information data API

"""
API service for describing detail movie information data 
with information about directors and actors written on DRF.
"""


### Installing using GitHub

- Python3 must be already installed
- Install PostgreSQL and create db

```shell
git clone https://github.com/Viktor-Beniukh/movies-infodata-api.git
cd movies-infodata-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   
```
You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;



## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`



## Getting access

- Create user via /user/register/
- Get access token via /user/token/



## Features

- JWT authentication;
- Admin panel /admin/;
- Documentation is located at /api/doc/swagger/;
- Creating category, genres, directors and actors;
- Creating movies with category, genres, directors and actors;
- Filtering movies by title, category, genres, year of release;
- Filtering directors & actors by name;
- Adding rating to movies;
- Leaving reviews to movies, commenting these reviews and adding comments to comments;


### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that 2 services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there;


### What do APIs do

- [GET] /movies/ - obtains a list of movies with the possibility of filtering by title, genres, categories, year of release;
- [GET] /directors/ - obtains a list of directors with the possibility of filtering by name;
- [GET] /actors/ - obtains a list of actors with the possibility of filtering by name;

- [GET] /movies/id/ - obtains the specific movie information data;
- [GET] /directors/id/ - obtains the specific director data;
- [GET] /actors/id/ - obtains the specific actor data;

- [POST] /actors/ - creates an actor;
- [POST] /directors/ - creates a director;
- [POST] /categories/ - creates a genre;
- [POST] /genres/ - creates a genre;
- [POST] /movies/ - creates a movie;
- [POST] /movie-frames/ - adds frames to movies;
- [POST] /ratings/ - adds rating to movies;
- [POST] /reviews/ - adds reviews to movies, comment to reviews and comment to comment;


- [GET] /user/me/ - obtains the specific user information data;

- [POST] /user/register/ - creates new users;
- [POST] /user/token/ - creates token pair for user;
- [POST] /user/token/refresh/ - gets new access token for user by refresh token;
- [POST] /user/token/verify/ - validates user access token;

- [POST] /user/me/profile-create/ - creates new user profiles;

- [PUT] /user/me/id/profile-update/ - updates user profile;


### Checking the endpoints functionality
- You can see detailed APIs at swagger page: `http://127.0.0.1:8000/api/doc/swagger/`.



## Testing

- Run tests using different approach: `docker-compose run app sh -c "python manage.py test"`;
- If needed, also check the flake8: `docker-compose run app sh -c "flake8"`.



## Check project functionality

- Note: after running project you need to set values to RatingStar model through admin panel(e.g. 1, 2, 3, 4, 5)

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.



## Create token pair for user

Token page: `http://127.0.0.1:8000/user/token/`

Enter:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.
