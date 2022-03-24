# camp-app

This project is aimed to manage the system for registering to the camp(s).

## Requirements

This project requires following software to run:

* Python v3.9.5
* [Pipenv](https://pipenv.pypa.io/en/latest/)
* Docker-Compose


### Init Setup

```bash
$ cd to/the/repository
$ git clone git@github.com:anton-pytel/camp-app.git
$ cd camp-app

$ pipenv --python 3.9 # This will create a virtual env for you
Creating a virtualenv for this project...

✔ Successfully created virtual environment!
Virtualenv location: /home/.../camp-app-bwAv4hx9
Creating a Pipfile for this project...
$ pipenv shell
$ pipenv sync #synchronize dependencies
$ source dev.env  #prepare env variables
$ docker-compose up -d camp-app-db  #setup database
$ cd app
$ python manage.py migrate # initialize database model (DDL)
$ python manage.py createsuperuser # create admin user
$ python manage.py runserver # access the url localhost:8000/admin

# in order to run gallery  https://github.com/Starcross/django-starcross-gallery
$ python manage.py makemigrations gallery
$ python manage.py migrate gallery
```

### Development and run

```bash
# activate virtual environment based on the location above eg.:
$ cd to/the/devrepository/
$ pipenv shell
$ source dev.env
# optionally - add dependency
$ pipenv install <> # <> replace with regular project lib dependency
$ pipenv install -d <> # <> replace with the development lib dependency
$ python app/manage.py runserver
# after changes in models
$ python app/manage.py makemigrations   
$ python app/manage.py migrate

```


### Deployment
- migration
- setup valid registration and prices
