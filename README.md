# Lightning Address Server

Lightning Address Server is a Flask-based server implementation to facilitate the receipt of payments via Lightning Network using human-readable identifiers following the [Lightning Address](https://lightningaddress.com/) protocol.

## Features
- LNURLp support for static Lightning addresses.

## Pre-requisites
- LND (Lightning Network Daemon) setup and running.
- nginx installed on your server.
- Python 3.6 or higher.

nginx Configuration
Create a new server block in your nginx configuration or edit the default one. Make sure to replace your-domain.com with your actual domain name.

server {
    listen 80;
    server_name your-domain.com;

    location /.well-known/lnurlp/ {
        proxy_pass http://localhost:5002;
    }

    location /lnurlp/ {
        proxy_pass http://localhost:5002;
    }
}


Test the configuration and reload nginx:
sudo nginx -t
sudo systemctl reload nginx
Usage
Run the Lightning Address Server:

python3 app.py
Your Lightning Address Server is now running. You can test it by visiting the following URL: http://your-domain.com/.well-known/lnurlp/your-username
