from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
 
#models.py資料表
from test01linebot.models import *
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':

        message=[]
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message.append(TextSendMessage(text=str(body)))
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            
            if isinstance(event, MessageEvent):
                if event.message.type=='text':
                    message.append(TextSendMessage(text='文字訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='image':
                    message.append(TextSendMessage(text='圖片訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='location':
                    message.append(TextSendMessage(text='位置訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='video':
                    message.append(TextSendMessage(text='影片訊息'))
                    line_bot_api.reply_message(event.reply_token,message)


                elif event.message.type=='sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='file':
                    message.append(TextSendMessage(text='檔案訊息'))
                    line_bot_api.reply_message(event.reply_token,message)
                
        return HttpResponse()
    else:
        return HttpResponseBadRequest()