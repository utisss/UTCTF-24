FROM nginx:1.21-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY GitWebsite.tar.gz GitWebsite.tar.gz
RUN tar -xzf GitWebsite.tar.gz -C /usr/share/nginx/html
