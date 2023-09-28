# Why three different images?

1. `prod.Dockerfile` image is for final deployment using `gunicorn`

2. `dev-static.Dockerfile` image is for testing using `flask` with the files being already copied to container

3. `dev-mount.Dockerfile` image is for testing using `flask` while your local files are mounted i.e. any change in local file will cause `flask` to reload the server

# Building the images

You will need to build the images if you make any changes to the poetry packages. Be sure to be in the `root` directory in when building these images.

## Development

### Static

```powershell
docker build  . -t flask-dev-static --no-cache -f .\docker\dev-static.Dockerfile
```

### Dynamic

```powershell
docker build  . -t flask-dev-mount --no-cache -f .\docker\dev-mount.Dockerfile
```

## Production

```powershell
docker build  . -t gunicorn-prod --no-cache -f .\docker\prod.Dockerfile
```

# Running the images in a container

Be sure to be in the `root` directory in when running these commands.

Some cool flags you can use here:
1. `--rm` : Automatically remove the container when it exits
2. `-t` : Allocate a pseudo-TTY
3. `-d` : Run container in background and print container ID

## Development

### Static

```powershell
docker run -p 80:80 flask-dev-static
```

### Dynamic

```powershell
docker run -p 80:80 -v $pwd\server\static:/server/static -v $pwd\server\templates:/server/templates -v $pwd\server\main.py:/server/main.py -v $pwd\server\database.py:/server/database.py -v $pwd\server\.env:/server/.env -v $pwd\server\config.yml:/server/config.yml flask-dev-mount
```

## Production

```powershell
docker run -p 80:80 gunicorn-prod
```
