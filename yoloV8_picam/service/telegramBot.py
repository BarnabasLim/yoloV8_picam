import telegram
from telegram import InputMediaPhoto

class TelegramBot:
    def __init__(self, token, channel_id):
        self.token=token
        self.channel_id=channel_id
        self.bot=telegram.Bot(token = self.token)
        self.imgList=[]
        
    def addImg(self, img_path=None, text=''):
        if img_path!=None:
            self.imgList.append(InputMediaPhoto(open(img_path,'rb'),caption=text))
            
    def sendImgList(self):
        try:
            overallCaption=self.imgList[len(self.imgList)-1].caption
            for idx, item in enumerate(self.imgList):
                if(idx==len(self.imgList)-1):
                    self.imgList[idx].caption=overallCaption
                else:
                    self.imgList[idx].caption=''
            self.bot.send_media_group(chat_id=self.channel_id, media=self.imgList)
            return True
        except Exception as e:
            print(e, 'here')
            return False
