FROM nginx


RUN rm /etc/nginx/conf.d/default.conf
COPY bass-app.conf /etc/nginx/conf.d/
COPY proxy-parameters /etc/nginx/


VOLUME /var/www/bass-app/static/
VOLUME /var/www/bass-app/media/
EXPOSE 80
