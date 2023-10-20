from flask import Flask, request, jsonify, render_template_string
import logging
import subprocess
import json
import asyncio

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.FileHandler('error.log'),
                              logging.StreamHandler()])

@app.route('/.well-known/lnurlp/<username>', methods=['GET'])
def lnurl_request(username):
    logging.info(f'Received LNURL request for {username}')
    callback_url = f'https://{request.host}/lnurlp/{username}/callback'
    metadata = json.dumps([
        ["text/identifier", f"{username}@yourdomain.com"],
        ["text/plain", "Sats for zero"]
    ])
    response_data = {
        'tag': 'payRequest',
        'callback': callback_url,
        'minSendable': 1000,
        'maxSendable': 100000000,
        'metadata': metadata,
    }
    logging.info(f'Responded to LNURL request for {username}')
    return jsonify(response_data)

@app.route('/lnurlp/<username>/callback', methods=['GET'])
def lnurl_callback(username):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response_data = loop.run_until_complete(create_invoice_forlnurl(username, request.args.get('amount')))
        return jsonify(response_data)
    finally:
        loop.close()

async def create_invoice_forlnurl(username, amount):
    logging.info(f'Received callback for {username} with amount {amount}')

    if not amount:
        logging.error(f'Bad Request: amount is required for {username}')
        return 'Bad Request: amount is required', 400

    command = f'lncli addinvoice --amt={int(amount) // 1000}'  # Convert msats to sats

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        logging.error(f'Error creating invoice for {username}: {stderr.decode()}')
        return 'Internal Server Error', 500

    invoice_data = json.loads(stdout)
    payment_request = invoice_data['payment_request']

    response_data = {
        'pr': payment_request,
        'routes': [],
    }
    logging.info(f'Responded to callback for {username} with amount {amount}')
    return response_data  # Return the response data directly

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
