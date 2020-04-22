#!/bin/sh

# nginx config
if [ ! -e /etc/nginx/conf.d/nginx.conf ]; then
    echo 'creating symlink for nginx config'
    ln -s /etc/nginx/conf.d/nginx.conf /home/box/web/etc/nginx.conf
fi

if  ! $(systemctl is-active --quiet nginx); then
    echo 'start nginx'
    service nginx start
fi

# mysql config
if  ! $(systemctl is-active --quiet mysql); then
    echo 'start mysql'
    service mysql start
fi

mysql -uroot -e "CREATE DATABASE IF NOT EXISTS qa;"
mysql -uroot -e "CREATE USER IF NOT EXISTS 'box'@'localhost' IDENTIFIED BY 'box';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON qa.* TO 'box'@'localhost' WITH GRANT OPTION;"

# start gunicorn
echo 'start gunicorn'
cd ask
gunicorn ask.wsgi
