# AORTIC ROOT

Backend API for AORTA.

# Setup

We are hosting a server on Heroku. For developers, you'll want to set up a local development server. 

## Local Development Server

First ensure you have Python 3 installed (we have tested with Python 3.6.8).

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

# Features and Roadmap

## Notes

- [X] Endpoint to get list of all notes, +/- spaced repetition information based on authentication
- [X] Search filter for list of notes
  - [ ] Extend search filter to note comments and/or questions
- [X] Endpoint to get individual note, +/- spaced repetition information based on authentication
- [X] Endpoint to add a note comment/contribution
- [X] Endpoint to add EMQs to notes (requires authentication)
- [ ] Endpoint to delete a note comment
- [ ] Endpoint to edit a note comment

## Questions

- [X] Endpoint to get an EMQ by ID
- [X] Endpoint to get a random list of question IDs with filters
- [X] Annotate EMQ choices with number of users choosing each option
- [X] Endpoint to submit a question response (requires auth)
- [X] Endpoint to like a question (requires auth) 
- [X] Endpoint to flag a question (requires auth)
- [X] Endpoint to comment on a question (requires auth)
- [ ] Endpoint to modify or delete a comment on a question
- [ ] Filter out questions with 3 or more flags
- [X] Get list of questions responses for a corresponding user
- [ ] Endpoint to calculate average accuracy for each specialty, and for each topic
- [ ] Endpoint to get list of submitted questions with likes number
- [ ] Endpoint to get accuracy Z-score

## Users

- [X] Endpoint to register
- [X] Endpoint to login
- [ ] Endpoint to delete account

## Cases

Still to be planned.
