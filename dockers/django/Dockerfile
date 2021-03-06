FROM ubuntu:16.04


# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-setuptools \
    python3-pip \
    supervisor \
    memcached \
    && rm -rf /var/lib/apt/lists/*


# Install Gunicorn and BassCloud dependencies
COPY tmp/requirements.txt /tmp/

RUN pip3 install --no-cache-dir 'gunicorn>=19.7,<19.8' && \
    pip3 install --no-cache-dir python-memcached && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY tmp/basscloud-dev.tar.gz /tmp/basscloud-dev.tar.gz

RUN pip3 install --no-cache-dir /tmp/basscloud-dev.tar.gz && \
    rm /tmp/basscloud-dev.tar.gz


# Create BassCloud Django project
RUN mkdir -p /var/www/basscloud && \
    mkdir -p /var/log/django/ && \
    mkdir -p /var/log/gunicorn/ && \
    django-admin startproject --template=/usr/local/lib/python3.5/dist-packages/basscloud/conf/project_template/ djproject /var/www/basscloud/


# Configure and initialize Webgis Django project
COPY settings_custom.py /var/www/basscloud/djproject/settings_custom.py
ENV PYTHONPATH $PYTHONPATH:/var/www/basscloud/
ENV DJANGO_SETTINGS_MODULE djproject.settings
ENV LANG C.UTF-8


VOLUME /var/www/basscloud/static/
VOLUME /var/www/basscloud/media/
EXPOSE 8000


COPY gunicorn_conf.py /var/www/basscloud/gunicorn_conf.py


# Configure Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]