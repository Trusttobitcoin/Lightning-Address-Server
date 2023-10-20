
# LightningID-Server

LightningID-Server is a Flask application designed to facilitate receiving payments on the Lightning Network using human-readable identifiers as per the [Lightning Address](https://lightningaddress.com/) protocol.

## Prerequisites

- A running LND (Lightning Network Daemon) setup.
- nginx installed on your server.
- Python 3.6 or higher.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/LightningID-Server.git
cd LightningID-Server
2. Install Dependencies
bash
Copy code
pip install flask
3. LND Configuration
Ensure your LND is properly set up and running. You will need the paths to your tls.cert, admin.macaroon files, and the gRPC endpoint (usually localhost:10009).

4. nginx Configuration
Create a new server block or edit an existing one in your nginx configuration. Replace your-domain.com with your actual domain name:

nginx
Copy code
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

bash
Copy code
sudo nginx -t
sudo systemctl reload nginx
Usage
Running the Server
bash
Copy code
python3 app.py
Now, the LightningID-Server is running on your machine. Test it by visiting the following URL: http://your-domain.com/.well-known/lnurlp/your-username

Contributing
Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License.
