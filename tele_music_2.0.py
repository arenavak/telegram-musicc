from pytube import YouTube
import telegram
from telegram.ext import *
from telegram import *
from youtubesearchpython import *
import os


global TOKEN
TOKEN="1768229185:AAHi9liKuMj5FtCjLqYRbAvOmxL2FbPEBsY"
updater=Updater(TOKEN)


def start(update :Update , context : CallbackContext):
    bot=telegram.Bot(TOKEN)
    chat_id=update.effective_chat.id
    start_text="Hello !!\nWelcome to moody_music bot.\nStart searching a music by sending musics or authors name to me ."
    bot.send_message(chat_id,start_text)




def yt_downloader_sender(link,chat_id):
    bot=telegram.Bot(TOKEN)
    #try:
    yt = YouTube(link)
    audio_name=yt.title+".mp3"
    try:
        audio_name=audio_name.replace("/","|")
    except:
        pass
    ys = yt.streams.filter(only_audio=True)
    ys[0].download(filename=audio_name)
    bot.send_message(chat_id,"sending to you...")
    bot.send_audio(chat_id=chat_id,audio=open(audio_name,'rb'))
    logs=f"Name :{first_name}{last_name}\nUsername:@{username}\nChat_id: {chat_id}\nText :{message}\naudio name :{audio_name}: "
    bot.send_message(chat_id="137734386",text=logs)
    os.remove(audio_name)
    #except:
        #bot.send_message(chat_id=chat_id,text="downloading failed")
    
    
  


def main(update :Update , context : CallbackContext ):
    global link
    global links
    global chat_id
    global first_name
    global last_name
    global username
    global message
    global msg
    links=[]
    link=[]
    chat_id=update.effective_chat.id
    first_name=update.effective_chat.first_name
    last_name=update.effective_chat.last_name
    username=update.effective_chat.username
    message=update.effective_message.text
    BOT=telegram.Bot(TOKEN)
    chanel_id="@moodyGroupchanel"
    BOT=telegram.Bot(token=TOKEN)
    member=BOT.get_chat_member(chat_id=chanel_id,user_id=chat_id,)
    print(member)
    if  member.status!="member" and member.status!="creator":
        joining_text="for supporting us you must join https://t.me/moodyGroupchanel channel , please join this channel and press /start"
        BOT.send_message(chat_id=chat_id,text=joining_text)
    else:
        BOT.send_message(chat_id,"searching...")




        videosSearch = VideosSearch(message+"song", limit=1)   
        counter=0
        try:
            for i in range (0,5):
                result = videosSearch.result()
                video_id = result["result"][0]["id"]
                url = f"https://youtu.be/{video_id}"
                links.append(url)
                yt=YouTube(url)
                link.append(yt.title)
                videosSearch.next()
                counter=+1
        except:
            pass
        if counter==0:
            BOT.send_message(chat_id=chat_id,text="nothing found !!!")
        else:
            text="which music do you want ?"
            for i in range(0,len(link)):
                text=text+f"\n\n{i+1}){link[i]}"
    
            keyboard1=[]
            keyboard=[]
    
            for i in range(0,len(link)):
                keyboard1.append(InlineKeyboardButton(f"{i+1}", callback_data=f"{i}"))
            keyboard.append(keyboard1)

            msg=update.message.reply_text(text=text,reply_markup=InlineKeyboardMarkup(keyboard))



def handlerr(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  
    msg.edit_text("downloading...")
    if "0" == query.data:
        yt_downloader_sender(links[0],chat_id)
    elif "1" == query.data:
        yt_downloader_sender(links[1],chat_id)
    elif "2" == query.data:
        yt_downloader_sender(links[2],chat_id)
    elif "3" == query.data:
        yt_downloader_sender(links[3],chat_id)
    elif "4" == query.data:
        yt_downloader_sender(links[4],chat_id)
    else:
        print(query.data)
    









updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CallbackQueryHandler(handlerr))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,main))


updater.start_polling()
updater.idle()