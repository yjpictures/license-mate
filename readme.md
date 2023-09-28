# What is this?

`Flask License Manager` is an open-source license manager that you can deploy easily in a variety of environments and customize to your own needs. This is made using `Flask` for `REST API` server and `MongoDB` for the database.

# How to deploy this license manager?

1. Use the docker image (coming soon!) and deploy it in your server environment.

2. Create a [`MongoDB Atlas`](https://www.mongodb.com/pricing) project/cluster and add the IP address(es) of the server into `MongoDB` (project -> security -> network access) for whitelisting (could also allow access from anywhere but its not recommended).

3. Customize the `.env` file based on your needs and that's it! Simple!

# Now, what about client side and documentation for API?

The documentation for all the REST API calls can be seen if you do a `GET` request `/` or you open the server URL on browser. `Flask License Manager` uses [`HTTP Basic Auth`](https://datatracker.ietf.org/doc/html/rfc7617) for authentication purposes. There are three different types of `users` one can use for different access levels - `admin`, `manager` and `client`.

# Want us to take care of hosting your license manager?

Coming soon!