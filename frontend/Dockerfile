# Get docker image
FROM debian:buster-slim

# Import groupid and host environment variable
ARG GROUPID
ARG DOMAIN
ARG URL_PREFIX
ARG PORT_PREFIX

# Install cordova
# Also install shelljs because of windows for some reason
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

# Set working dir
WORKDIR /app

# Transfer all our stuff to the builder
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN npm install -g cordova && npm install shelljs

COPY . /app/

# Set the host variable in default.js (overwrite)
RUN echo "const HOST = '${URL_PREFIX}${DOMAIN}:${PORT_PREFIX}${GROUPID}';" > ./www/scripts/defaults.js

# Run cordova app
CMD [ "cordova", "run", "browser", "--release", "--port=3000" ]
