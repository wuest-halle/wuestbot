FROM nginx:latest

COPY website /var/www/website/
COPY nginx.conf /etc/nginx
COPY fullchain.pem /var/www/certs/
COPY privkey.pem /var/www/certs/

EXPOSE 443
