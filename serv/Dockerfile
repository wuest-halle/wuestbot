FROM nginx:latest

WORKDIR .

COPY nginx.conf /etc/nginx/
COPY website /var/www/website/
# COPY fullchain.pem /var/www/certs/
# COPY privkey.pem /var/www/certs/

EXPOSE 443
