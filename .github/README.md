# 🌐🔗 [licensemate.ca](https://licensemate.effectuatecorp.com)

[![Version](https://img.shields.io/docker/v/yjpictures/license-mate/latest)](https://github.com/yjpictures/license-mate/pkgs/container/license-mate)
[![License](https://img.shields.io/github/license/yjpictures/license-mate)](https://github.com/yjpictures/license-mate/blob/master/LICENSE)
[![GitHub](https://img.shields.io/badge/github-black?logo=github)](https://github.com/yjpictures/license-mate)
[![Docker Pulls](https://img.shields.io/docker/pulls/yjpictures/license-mate?logo=docker)](https://hub.docker.com/r/yjpictures/license-mate)
[![X (formerly Twitter)](https://img.shields.io/twitter/follow/license_mate?label=X%20(formerly%20twitter))](https://twitter.com/license_mate)
[![LinkedIn](https://img.shields.io/badge/linkedin-blue?logo=linkedin)](https://www.linkedin.com/showcase/license-mate)
[![Reddit](https://img.shields.io/badge/reddit-orange?logo=reddit&logoColor=white)](https://www.reddit.com/user/license-mate)



# What is this?

`License Mate` is an open-source software license manager that you can deploy easily in a variety of environments and customize to your own needs. This is made using `Flask` for `REST API` server, `React.js` for the server UI and `MongoDB` for the database.

`License Mate` is a tool or system designed to help organizations and individuals manage the distribution, tracking, and compliance of software licenses. It serves as a central hub for controlling how software licenses are allocated, monitored, and maintained for a software. Here's a breakdown of its key functions:

1. License Creation and Allocation
2. License Tracking
3. License Validation
4. License Renewal
5. License Deactivation and Removal



## Who is this for?

Companies and individuals who develop and distribute software products can use `License Mate` to control access and distribution of their software.



# How to deploy this license manager?

## Method 1: Self-hosted server and Cloud MongoDB (preferred)

**This method is preferred as `MongoDB Atlas` has data redundancy built-in.**

1. Create the following `docker compose` on your server and name it `compose.yml`.

```yml
name: license-mate

services:

  backend:
    image: yjpictures/license-mate:1.1
    container_name: backend
    ports:
      - 80:80
    environment:
      MONGODB_URI: mongodb+srv://<username>:<password>@<yourcluster>.mongodb.net/
      ADMIN_PWD: <admin_password>
      MANAGER_PWD: <manager_password>
      CLIENT_PWD: <client_password>
      REQUIRED_CREATE: name, email, company, product, machine-node, machine-sn
      UNIQUE_VALIDATE: email, machine-node, machine-sn
```

2. Create a [`MongoDB Atlas`](https://www.mongodb.com/pricing) project/cluster and add the IP address(es) of the server into `MongoDB` (project -> security -> network access) for whitelisting (could also allow access from anywhere but its not recommended).

3. Customize the environment variables based on your needs, `MONGODB_URI` is a connection string that can be obtained from your `MongoDB` project.

4. Run `docker compose up` in your server to pull the image and run it into a container.

*Simple as that! License Mate server should now be running on your `port 80`.*


## Method 2: Self-hosted server and MongoDB

1. Create the following `docker compose` on your server and name it `compose.yml`.

```yml
name: license-mate

services:

  backend:
    image: yjpictures/license-mate:1.1
    container_name: backend
    ports:
      - 80:80
    environment:
      ADMIN_PWD: <admin_password>
      MANAGER_PWD: <manager_password>
      CLIENT_PWD: <client_password>
      REQUIRED_CREATE: name, email, company, product, machine-node, machine-sn
      UNIQUE_VALIDATE: email, machine-node, machine-sn
    networks:
      - backend-network
    depends_on:
      - database

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
    name: license-mate
    driver: bridge
```

2. Customize the environment variables based on your needs.

3. Run `docker compose up` in your server to pull the image and run it into a container.

*Simple as that! License Mate server should now be running on your `port 80`.*


## Method 3: Installer files (coming soon)

Coming soon! You would soon be able to install everything through an installer file.



# What about client side and documentation for API?

The interactive documentation for all the REST API calls can be seen if you open the server URL on a browser. You will be able to see all the different requests you can send including the required parameters, JSON payload schema and expected output. You can even test out the requests right through the browser window.

`License Mate` uses [`HTTP Basic Auth`](https://datatracker.ietf.org/doc/html/rfc7617) for authentication purposes.

Route `/ui` after the server URL will allow users to open Admin section, where admins can manage the licenses through the web browser.



# Want us to take care of hosting your license manager?

Depending on the size and scale, we can host, manage and customize License Mate to suit your needs so you can focus on the client side of things.

[Contact us for more information!](mailto:licensemate@effectuatecorp.com)
