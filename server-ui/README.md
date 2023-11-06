# How does it work?

Server UI is made using ReactJS and is served in production by the Flask Server.

The development is done using node and you can see the changes in the web app immediately after code changes.

All the commands mentioned here are to be run from inside `/server-ui` directory.

# Development

## First time dev setup

To install all the dependencies

```bash
npm i
```

Make sure the base url in `src/Api.js` is set to `baseURL: 'http://localhost/api/v1/'` if you are running flask server locally.

## Run the node server for development

```bash
npm start
```

## How to add packages

```bash
npm i <package>
```

## How to remove packages

```bash
npm uninstall <package>
```

# Production

## Build

Make sure the base url in `src/Api.js` is set to `baseURL: '/api/v1/'`.

```bash
npm i --omit=dev
npm run build
```

This will create a `server-ui.js` in `/server/static/js` directory which is then used in `server-ui.html` template and is served by the Flask server.