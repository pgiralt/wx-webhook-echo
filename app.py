from flask import Flask, request
from bot import handle_webhook, set_up_webhooks

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Echo bot is UP'


@app.route('/webhook', methods=['POST'])
def process_webhook():
    json_data = request.json
    result = handle_webhook(json_data)

    return result


def init():
    result = set_up_webhooks()
    print(result)

init()

if __name__ == '__main__':
    app.run()
