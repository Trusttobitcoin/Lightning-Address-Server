# LightningID-Server

LightningID-Server is a Flask application designed to facilitate receiving payments on the Lightning Network using human-readable identifiers as per the [Lightning Address](https://lightningaddress.com/) protocol.

## Prerequisites

- A running LND (Lightning Network Daemon) setup.
- nginx installed on your server. Configure it using the following setup:
- Create a new server block or edit an existing one in your nginx configuration. Replace your-domain.com with your actual domain name:
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

    Test and reload nginx configuration:
    sudo nginx -t
    sudo systemctl reload nginx
  
- Python 3.6 or higher.

## Usage
Running the Server
python3 app.py


