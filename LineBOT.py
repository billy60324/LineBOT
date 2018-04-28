from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('IvP19kRz9Zu4Kr0Y/3pGz2Vuc02JjWN1I4fS/1xnFebLos+AVVj05VTfL5CaAs+NfzAOVaYMJq1RmGxNSIBau7Xdi5vZRtkL41noO2xZ6zT/ZJxlwoIRWn5nXiHRXqvb3TBr39iVMtsiX7tMw9Z78gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bf73af9b5870cece6813088658ef6545')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
