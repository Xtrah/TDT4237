# Webserver running nginx
FROM nginx:perl

# Import groupid environment variable
ENV GROUPID=${GROUPID}
ENV PORT_PREFIX=${PORT_PREFIX}

# Copy nginx config to the container

COPY /certs/nginx-selfsigned.crt   /etc/nginx/ssl/cert.pem 
COPY /certs/nginx-selfsigned.key   /etc/nginx/ssl/privkey.pem
COPY nginx.conf /etc/nginx/nginx.conf