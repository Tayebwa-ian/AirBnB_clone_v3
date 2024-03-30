#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    # Install nginx
    sudo apt update
    sudo apt install nginx -y
fi
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
sym_link="/data/web_static/current"
if [ -L "$sym_link" ]; then
    sudo rm "$sym_link"
fi
sudo ln -s /data/web_static/releases/test "$sym_link"
sudo chown -R ubuntu:ubuntu /data
echo "Hello Holberton School" > /data/web_static/releases/test/index.html
content="\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}"
sudo sed -i "/\tserver_name _;/a \\${content}" /etc/nginx/sites-available/default
sudo service nginx restart
