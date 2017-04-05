FROM nginx


RUN rm /etc/nginx/conf.d/default.conf
COPY basscloud.conf /etc/nginx/conf.d/
COPY proxy-parameters /etc/nginx/


VOLUME /var/www/basscloud/static/
VOLUME /var/www/basscloud/media/
EXPOSE 80
