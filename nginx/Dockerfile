FROM nginx:stable-alpine

RUN apk add --no-cache openssl

WORKDIR /etc/nginx
COPY nginx.conf /etc/nginx/nginx.conf
COPY openssl.cnf /etc/nginx/openssl.cnf

RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 \
      -newkey rsa:2048 \
      -keyout /etc/nginx/ssl/wattwatcher.key \
      -out /etc/nginx/ssl/wattwatcher.crt \
      -config /etc/nginx/openssl.cnf

EXPOSE 80 443
