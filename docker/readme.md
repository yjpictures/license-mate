# Why docker?

> Docker streamlines the development lifecycle by allowing developers to work in standardized environments using local containers which provide your applications and services. Containers are great for continuous integration and continuous delivery (CI/CD) workflows.

# How to use docker for flask license manager?

## Method 1: Dockerfile

You could use one of the three provided `Dockerfile`s in the directory `./docker/builds/` to create your own image. Instructions on how to do so are in a separate readme in the `builds` folder.

## Method 2: Docker Compose

You could choose from the six `docker compose` files to easily spin up a container. Simply pick one of the file you want to start with and run the following command at the `root` directory.

```PowerShell
docker compose -f .\docker\<local/cloud>-MongoDB\<your-choice>.yml up
```

`dev-mount.yml` is for testing using `Flask` while your local files are mounted i.e. any change in local file will cause `Flask` to reload the server, whereas `dev-static.yml` is for testing using `Flask` with the files being already copied into the image.

You can choose amongst the following options for database:

### 1. Cloud MongoDB Server

This will require you to create a [`MongoDB Atlas`](https://www.mongodb.com/pricing) project/cluster and enter the connection string into the environment file.

### 2. Local MongoDB Server

No setup for setting up the MongoDB is required, its all done through `docker`.