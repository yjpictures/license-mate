# Why three different images?

1. `prod.Dockerfile` image is for final deployment using `gunicorn`

2. `dev-static.Dockerfile` image is for testing using `Flask` with the files being already copied into the image

3. `dev-mount.Dockerfile` image is for testing using `Flask` while your local files are mounted i.e. any change in local file will cause `Flask` to reload the server

# Building the images

You will need to build the images if you make any changes to the poetry packages. Be sure to be in the `root` directory in when building these images.

Some cool flags you can use here:
1. `-t` : Name and optionally a tag in the `name:tag` format
2. `--no-cache` : Do not use cache when building the image
3. `-f` : Name of the Dockerfile (Default is `PATH/Dockerfile`)

## Development

### Static

```PowerShell
docker build  . -t flask-dev-static --no-cache -f .\docker\builds\dev-static.Dockerfile
```

### Dynamic

```PowerShell
docker build  . -t flask-dev-mount --no-cache -f .\docker\builds\dev-mount.Dockerfile
```

## Production

```PowerShell
docker build  . -t gunicorn-prod --no-cache -f .\docker\builds\prod.Dockerfile
```

# Running the images in a container

Be sure to be in the `root` directory in when running these commands.

Some cool flags you can use here:
1. `--rm` : Automatically remove the container when it exits
2. `-t` : Allocate a pseudo-TTY
3. `-d` : Run container in background and print container ID
4. `--env-file` : Read in a file of environment variables

## Development

### Static

```PowerShell
docker run -p 80:80 --env-file <env-file-path> flask-dev-static
```

### Dynamic

We are not supplying `--evn-file` tag as the `.env` file should already exist in your `/server/` directory because of mounting.
```PowerShell
docker run -p 80:80 -v $pwd\server\static:/server/static -v $pwd\server\templates:/server/templates -v $pwd\server\main.py:/server/main.py -v $pwd\server\database.py:/server/database.py -v $pwd\server\.env:/server/.env -v $pwd\server\config.yml:/server/config.yml flask-dev-mount
```

## Production

```PowerShell
docker run -p 80:80 --env-file <env-file-path> gunicorn-prod
```
