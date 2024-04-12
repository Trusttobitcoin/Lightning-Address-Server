from flask import Flask, request, jsonify
import subprocess
import json
import logging
import uuid
import asyncio

app = Flask(__name__)
active_uuids = {}
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.FileHandler('error.log'),
                              logging.StreamHandler()])

async def create_invoice_forlnurl(username, amount):
    logging.info(f'Received callback for {username} with amount {amount}')

    if not amount:
        logging.error(f'Bad Request: amount is required for {username}')
        return 'Bad Request: amount is required', 400

    # Modify the command to include lncli with the specified parameters
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
    return response_data

@app.route('/.well-known/lnurlp/<username>', methods=['GET'])
def lnurl(username):

    logging.info(f"Received LNURL request for {username}")
    unique_id = str(uuid.uuid4())
    active_uuids[unique_id] = {'username': username}

    callback_url = f"https://{request.host}/lnurlp/{username}/callback/{unique_id}"
    response_data = {
        "callback": callback_url,
        "maxSendable": 1000000,
        "minSendable": 1000,
        "metadata": f'[[\"text/plain\", \"Send sats to {username} in Wallet Of Learning\"]]',
        "tag": "payRequest"
    }
    logging.info(f"Responded to LNURL request for {username}")
    return jsonify(response_data)

@app.route('/lnurlp/<username>/callback/<unique_id>', methods=['GET'])
async def lnurl_callback(username, unique_id):
    if unique_id not in active_uuids or active_uuids[unique_id]['username'] != username:
        return jsonify({"status": "ERROR", "reason": "Invalid request"}), 400

    amount = int(request.args.get('amount'))  
    comment = request.args.get('comment', '')  
    sats_amount = amount // 1000
    if sats_amount > 1000:
        active_uuids.pop(unique_id, None)  
        return jsonify({"status": "ERROR", "reason": "More than 1000 sats not allowed in beta version"}), 400
    logging.info(f"Received callback for {username} with amount {amount}")
    # Create an invoice using lncli
    invoice_data = await create_invoice_forlnurl(username, amount)
    return jsonify(invoice_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
