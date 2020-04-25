#!/bin/sh

# nginx config
if [ ! -L /etc/nginx/conf.d/nginx.conf ]; then
    echo 'creating symlink for nginx config'
    ln -s /home/box/web/etc/nginx.conf /etc/nginx/conf.d/nginx.conf 
fi

echo 'start nginx'
service nginx start
nginx -s reload

# mysql config
echo 'start mysql'
service mysql start

mysql -uroot -e "CREATE DATABASE IF NOT EXISTS qa;"
# mysql -uroot -e "CREATE USER IF NOT EXISTS 'box'@'localhost' IDENTIFIED BY 'box';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON qa.* TO 'box'@'localhost' WITH GRANT OPTION;"

# start gunicorn
echo 'start gunicorn'
cd ask
./manage.py makemigrations 
./manage.py migrate
gunicorn ask.wsgi
