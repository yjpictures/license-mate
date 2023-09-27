# Development

## First time dev setup

This will create and activate the virtual environment - `poetry shell`

This will install all dependencies - `poetry install`

```PowerShell
poetry shell
poetry install
```

## Run the flask server for development
Make sure poetry environment is enabled, then run the following code

```PowerShell
flask --app main run --debug --port 80
```

## How to add packages

```PowerShell
poetry add <package>
poetry add <package> --group prod
```

## How to remove packages

```PowerShell
poetry remove <package>
```

## Sample .env file

```env
FLASK_ENV=development
MONGODB_URI=mongodb+srv://<username>:<password>@<yourcluster>.mongodb.net/
LICENSE_LEN=16
ADMIN_PWD=<admin_password>
MANAGER_PWD=<manager_password>
CLIENT_PWD=<client_password>
```

# Production

## Deployment

```PowerShell
poetry install --with prod
gunicorn main:app
```
