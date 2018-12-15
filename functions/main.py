import os
from dotenv import load_dotenv
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, ImageMessage, TextSendMessage)

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
image_path = os.path.join(os.getcwd(), "image.jpg")

def LineBot(request):
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
      handler.handle(body, signature)
    except InvalidSignatureError:
      abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text)
  )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
  message_content = line_bot_api.get_message_content(event.message.id)

  with open(image_path, 'wb') as fd:
    for chunk in message_content.iter_content():
        fd.write(chunk)
