# Development

## First time dev setup

This will create and activate the virtual environment - `poetry shell`

This will install all dependencies - `poetry install`

```
poetry shell
poetry install
```

## Run the flask server for development
Make sure poetry environment is enabled, then run the following code

```
flask --app main run --debug --port 80
```

## How to add packages

```
poetry add <package>
poetry add <package> --group prod
```

## How to remove packages

```
poetry remove <package>
```

## Sample .env file

```
FLASK_ENV=development
MONGODB_URI=mongodb+srv://<username>:<password>@<yourcluster>.mongodb.net/
LICENSE_LEN=16
```

# Production

## Deployment

```
poetry install --with prod
gunicorn main:app
```
