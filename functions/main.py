import os
from dotenv import load_dotenv
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, ImageMessage, TextSendMessage)
from binbuddy import BinBuddy

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
image_path = os.path.join(os.getcwd(), "image.jpg")
binbuddy = BinBuddy(config={
  "rekognition": {
    "aws_access_key_id": os.getenv('AWS_ACCESS_KEY_ID'),
    "aws_secret_access_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
    "region_name": os.getenv('REGION_NAME')
  }
})

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
    TextSendMessage(text=binbuddy.which_bin_to_thrash_word(event.message.text))
  )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
  message_content = line_bot_api.get_message_content(event.message.id)

  image = bytearray()
  for chunk in message_content.iter_content():
    image.extend(chunk)
  
  labels = binbuddy.which_bin_to_thrash_image(image)
  if labels == "":
    labels = "ไม่พบข้อมูลประเภทขยะในฐานข้อมูล"
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=labels)
  )