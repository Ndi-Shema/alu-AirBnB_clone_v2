#!/usr/bin/env bash
#Update the package list and install Nginx

sudo apt update
sudo apt install -y nginx

# Create directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a basic HTML file
echo "<html>
  <head>
  </head>
  <body>
    Test this Nginx
  </body>
</html>" >/data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership and permissions
sudo chown -R ubuntu:ubuntu /data

# Configure Nginx to serve the static file
sudo sed -i '37i\\n\tlocation /hbnb_static {\n        alias /data/web_static/current/;\n    }' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
