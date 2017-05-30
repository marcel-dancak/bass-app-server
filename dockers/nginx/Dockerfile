FROM nginx


RUN rm /etc/nginx/conf.d/default.conf
COPY basscloud.conf /etc/nginx/conf.d/
# COPY certbot.conf /etc/nginx/conf.d/
COPY proxy-parameters /etc/nginx/
COPY ssl.conf /etc/nginx/


VOLUME /var/www/basscloud/files/
VOLUME /var/www/basscloud/media/
VOLUME /etc/letsencrypt/
VOLUME /var/www/certbot/


EXPOSE 80 443
