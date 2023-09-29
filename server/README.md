# Preface

It is preferred to use containers, kindly refer to the `readme.md` in `/docker` directory.

If you still prefer to do development on your local environment, read along. All the commands mentioned here are to be run from inside `/server` directory.

# Development

## First time dev setup

This will create and activate the virtual environment - `poetry shell`

This will install all dependencies - `poetry install --without prod`

```PowerShell
poetry shell
poetry install --without prod
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

The `.env` file goes in `/server` directory.

```env
# =========================
# OPTIONAL FIELDS
# =========================
# This is for the name of MongoDB database
SERVER_ENV=development # default: production
# -------------------------
# This is for the auto-generated license key length
LICENSE_LEN=16 # default: 32
# -------------------------
# This is the connection string for MongoDB database
MONGODB_URI=mongodb+srv://<username>:<password>@<yourcluster>.mongodb.net/ # default: mongodb://database:27017/
# -------------------------

# =========================
# PASSWORDS FOR REST APIs
# =========================
# This user type can create, validate, update, get-all, delete a license
ADMIN_PWD=<admin_password>
# -------------------------
# This user type can create, validate, update, delete a license
MANAGER_PWD=<manager_password>
# -------------------------
# This user type can validate a license
CLIENT_PWD=<client_password>
# -------------------------

# =========================
# USER CONFIGURABLE SECTION
# =========================
# These are the fields that will be created for each license
REQUIRED_CREATE=name, email, company, product, machine-node, machine-sn
# -------------------------
# These are the fields that are used to check if a new license is unique or not
# If ANY of these fields have duplicate values in database then a license will not be created
# These fields SHOULD be in the 'REQUIRED_CREATE' and should match the case
UNIQUE_VALIDATE=email, machine-node, machine-sn
# -------------------------
```

# Production

## Deployment

```PowerShell
poetry install --with prod
gunicorn main:app
```
