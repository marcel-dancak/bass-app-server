FROM ubuntu:16.04


# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-pip \
    supervisor \
    && rm -rf /var/lib/apt/lists/*



COPY bass-app-dev.tar.gz /tmp/bass-app-dev.tar.gz

# Install Gunicorn and BassApp dependencies
RUN pip3 install --no-cache-dir 'gunicorn>=19.7,<19.8' && \
    pip3 install --no-cache-dir /tmp/bass-app-dev.tar.gz && \
    rm /tmp/bass-app-dev.tar.gz

# Install Gunicorn and BassApp dependencies
# RUN pip3 install --no-cache-dir 'gunicorn>=19.1.1,<19.2' && \
#     pip3 install 'https://github.com/marcel-dancak/bass-app-server/zipball/master#egg=bass-app-server&subdirectory=server'


# Create BassApp Django project
RUN mkdir -p /var/www/bass-app && \
    mkdir -p /var/log/django/ && \
    mkdir -p /var/log/gunicorn/ && \
    django-admin startproject --template=/usr/local/lib/python3.5/dist-packages/bassapp/conf/project_template/ djproject /var/www/bass-app/


# Configure and initialize Webgis Django project
COPY settings_custom.py /var/www/bass-app/djproject/settings_custom.py
ENV PYTHONPATH $PYTHONPATH:/var/www/bass-app/
ENV DJANGO_SETTINGS_MODULE djproject.settings


# ARG CACHEBUST=1
# RUN django-admin collectstatic --no-input


VOLUME /var/www/bass-app/static/
VOLUME /var/www/bass-app/media/
EXPOSE 8000


COPY gunicorn_conf.py /var/www/bass-app/gunicorn_conf.py


# Configure Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]