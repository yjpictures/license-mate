# What is this?

`Flask License Manager` is an open-source license manager that you can deploy easily in a variety of environments and customize to your own needs. This is made using `Flask` for `REST API` server and `MongoDB` for the database.

<u>Links</u>

- [Docker Hub](https://hub.docker.com/r/yjpictures/flask-license-manager)
- [GitHub Container Registry](https://ghcr.io/yjpictures/flask-license-manager)
- [GitHub](https://github.com/yjpictures/flask-license-manager)



# How to deploy this license manager?

## Method 1: Self-hosted server and Cloud MongoDB (preferred)

**This method is preferred as `MongoDB Atlas` has data redundancy built-in.**

1. Create the following dockerfile on your server and name it `compose.yml`.

```yml
name: 'flask-license-manager'

services:

  backend:
    image: yjpictures/flask-license-manager
    container_name: backend
    ports:
      - '80:80'
    environment:
      MONGODB_URI: mongodb+srv://<username>:<password>@<yourcluster>.mongodb.net/
      ADMIN_PWD: <admin_password>
      MANAGER_PWD: manager_password>
      CLIENT_PWD: client_password>
      REQUIRED_CREATE: name, email, company, product, machine-node, machine-sn
      UNIQUE_VALIDATE: email, machine-node, machine-sn
```

2. Create a [`MongoDB Atlas`](https://www.mongodb.com/pricing) project/cluster and add the IP address(es) of the server into `MongoDB` (project -> security -> network access) for whitelisting (could also allow access from anywhere but its not recommended).

3. Customize the environment variables based on your needs, `MONGODB_URI` is a connection string that can be obtained from your `MongoDB` project.

4. Run `docker compose up` in your server to pull the image and run it into a container.

*Simple as that! Flask License Manager server should now be running on your `port 80`.*


## Method 2: Self-hosted server and MongoDB

1. Create the following dockerfile on your server and name it `compose.yml`.

```yml
name: 'flask-license-manager'

services:

  backend:
    image: yjpictures/flask-license-manager
    container_name: backend
    ports:
      - '80:80'
    environment:
      ADMIN_PWD: <admin_password>
      MANAGER_PWD: manager_password>
      CLIENT_PWD: client_password>
      REQUIRED_CREATE: name, email, company, product, machine-node, machine-sn
      UNIQUE_VALIDATE: email, machine-node, machine-sn
    networks:
      - backend-network

  database:
    image: mongo:6.0
    container_name: database
    environment:
      MONGODB_DATA_DIR: /data/db
      MONDODB_LOG_DIR: /dev/null
    volumes:
      - licenseDB:/data/db
    networks:
      - backend-network

volumes:
  licenseDB:
    name: licenseDB
    driver: local

networks:
  backend-network:
    name: flask-license-manager
    driver: bridge
```

3. Customize the environment variables based on your needs.

4. Run `docker compose up` in your server to pull the image and run it into a container.

*Simple as that! Flask License Manager server should now be running on your `port 80`.*


## Method 3: Installer files (coming soon)

Coming soon! You would soon be able to install everything through an installer file.



# What about client side and documentation for API?

The documentation for all the REST API calls can be seen if you do a `GET` request `/` or you open the server URL on browser. `Flask License Manager` uses [`HTTP Basic Auth`](https://datatracker.ietf.org/doc/html/rfc7617) for authentication purposes. There are three different types of `users` one can use for different access levels - `admin`, `manager` and `client`.



# Want us to take care of hosting your license manager?

Depending on the size and scale, we can host, manage and customize the flask license manager to suit your needs so you can focus on the client side of things.

[Contact us for more information!](mailto:hello@yashj.ca)
