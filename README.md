# AORTIC ROOT

Backend API for AORTA.

# Setup

We are hosting a server on Heroku. For developers, you'll want to set up a local development server. 

## Local Development Server

First ensure you have Python 3 installed (we have tested with Python 3.7.5).

To set up this backend locally, clone this repository.

```sh
git clone https://github.com/cigmah/aorticroot.git
```

Next, you will need to set an environment variable, `SECRET_KEY`. 
[Please refer to the official Django documentation](https://docs.djangoproject.com/en/2.2/ref/settings/#secret-key). 

If you are running the server locally, an SQLite database is probably sufficient
for testing. Create a `.env` file in the root directory with the following
contents:

``` 
DATABASE_URL=sqlite:///db.sqlite3
```

This will save the database to a file named `db.sqlite3` in the root directory.

It's highly recommended you use a virtual environment to run the backend. 
Read more on virtual environments at [the official Python
documentation.](https://docs.python.org/3.6/tutorial/venv.html)

After activating your virtual environment, install the requirements from `requirements.txt`:

```sh
pip install -r requirements.txt
```

Then, run your first migrations to initialise the database.

``` sh
python manage.py migrate
```

Next, create an administrator account for use with the administrator interface.

``` sh
python manage.py createsuperuser
```

Finally, run the tests to make sure things are going smoothly.

``` sh
python manage.py test
```

If all tests pass, you should be good to go. Start the development server with:

``` sh
python manage.py runserver
```

Note that you may encounter a `500 Internal Server` error when Debug = False, in which case try running:

``` sh
python manage.py collectstatic
```

## Cases

Still to be planned.
