# AORTIC ROOT

Backend API for AORTA.

# Setup

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

# Roadmap

- Tags
  - [ ] Implement and test filtering questions by arbitrary tags
  - [ ] Enforce lowercase for easy matching?
- Choices
  - [ ] Implement and test filtering questions by answer
  - [ ] Enforce lowercase for easy matching?
  - [ ] Add metadata to choices e.g. short descriptions?
  - [ ] Random generation of distractors within category, or expose endpoint to
        get random choices per category
- Questions
  - [ ] Return choice statistics with question (annotate with sum over
        QuestionResponse table)
  - [ ] Implement simple spaced repetition algorithm for authenticated users
        (select from QuestionResponse where user = request.user and question_id
        = request.data.question_id, then fold left a two input algorithm?
        alternatively, save ease factor and interval with each new response)
  - [ ] Expose an endpoint for random questions (completely random if guest, or
        random with spaced repetition if authenticated)
- Cases
  - [ ] Add case table (need to spec first to determine what the frontend will need)
- Users
  - [ ] Friendlier random passwords (correct horse battery staple?)
  - [ ] Specify token expiry
  - [ ] Protect against spammed user account generation? Would prefer not
        storing *any* data about users (hence the no-email,
        we-give-you-a-password-and-you-cant-set-it-yourself auth system). 
- Documenation
  - [ ] Proper Swagger API
  - [ ] Comments in code.
