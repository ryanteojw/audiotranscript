FROM node:22.14.0 AS build

# set the working directory in the container
WORKDIR /app

# copy package.json and package-lock.json and install dependencies
COPY package*.json ./
RUN npm install

# copy the entire project
COPY . .

# build the Vue.js application
RUN npm run build

# use Node.js to serve the static files
FROM node:22.14.0

# set the working directory
WORKDIR /app

# copy the built app
COPY --from=build /app/dist /app/dist

# install a simple HTTP server to serve the static files
RUN npm install -g http-server

# expose the port the app will run on
EXPOSE 8080

# Command to run the app using the HTTP server
CMD ["http-server", "dist", "-p", "8080"]
