# Flask To-Do
I did this project to learn how to use Flask and Redis
and I decided to release the code as it may be useful
to others who are also learning.

## Features
- Simple and easy to understand Redis CRUD API.
- Custom error handling.
- User-friendly UI (_Using Bootstrap v5_).

---

## Usage
> **New to Redis? Look at the [Documentation](https://redis.io/documentation).**
> 
> **New to Flask? Look at the [Documentation](https://flask.palletsprojects.com/en/master/).**
> 
> **New to Bootstrap v5? Look at the [Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/).**

### Installation
#### System-side
This project requires Redis to function properly.
If you don't have it installed, please [Download Redis](https://redis.io/download).

#### Python-side
This project uses `pipenv` to handle its dependencies.
If you don't have it installed, use the following command.
```sh
pip3 install --user pipenv
```

To install the dependencies use the following command.
```sh
pipenv install
```

### Running the server
First we need to run our redis server
```sh
redis-server
```

Next, we run our Flask server using pipenv.
```sh
# We export the FLASK_APP variable
export FLASK_APP=app.py

# Run within the virtual environment
pipenv shell
python3 app.py

# Run outside the virtual environment
pipenv run python3 app.py
```

## License
Flask To-Do is distributed under [WTFPL License](./LICENSE).
