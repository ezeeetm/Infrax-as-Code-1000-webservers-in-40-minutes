#!/bin/bash
# update package lists and get dependencies
apt-get update
apt-get install -y nginx
service nginx stop # otherwise it will go into service behind ELB with nginx splash screen
apt-get install -y nginx uwsgi uwsgi-plugin-python python-pip git
pip install virtualenv

# grab our code
git clone https://github.com/ezeeetm/Infrax-as-Code-1000-webservers-in-40-minutes.git

# set up filesystem and virtualenv
mkdir -p /var/www/myapp
virtualenv /var/www/myapp/env
source /var/www/myapp/env/bin/activate
pip install bottle boto3 requests
deactivate
chown -R www-data:www-data /var/www/myapp

# copy files from local git repo out to where they belong on the filesystem
cp -f /Infrax-as-Code-1000-webservers-in-40-minutes/environment/default /etc/nginx/sites-enabled/default
cp -f /Infrax-as-Code-1000-webservers-in-40-minutes/environment/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini
cp -f /Infrax-as-Code-1000-webservers-in-40-minutes/index.py /var/www/myapp/index.py
cp -f /Infrax-as-Code-1000-webservers-in-40-minutes/index.html /var/www/myapp/index.html

# restart services to load new configs and engage uwsgi to our app
service nginx start
service uwsgi restart