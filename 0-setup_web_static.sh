#!/usr/bin/env bash
# Check if nginx is installed, and install it if not
if ! dpkg -s nginx &> /dev/null; then
  sudo apt-get update
  sudo apt-get -y install nginx
fi

# Create directories for web static content
sudo mkdir -p /var/www/html/hbnb_static/releases/test/
sudo mkdir -p /var/www/html/hbnb_static/shared/

# Create a symbolic link for web static content
sudo ln -sf /var/www/html/hbnb_static/releases/test/ /var/www/html/hbnb_static/current

# Create an index.html file with test content
sudo sh -c 'echo "<html><head><title>Test page</title></head><body><p>This is a test page.</p></body></html>" > /var/www/html/hbnb_static/releases/test/index.html'

# Set ownership for directories
sudo chown -R www-data:www-data /var/www/html/hbnb_static

# Add location block for web static content to the nginx config
sudo sh -c 'echo "location /hbnb_static/ {\n\talias /var/www/html/hbnb_static/current/;\n}\n" > /etc/nginx/sites-available/hbnb_static'
sudo ln -sf /etc/nginx/sites-available/hbnb_static /etc/nginx/sites-enabled/hbnb_static
sudo nginx -t && sudo systemctl reload nginx
