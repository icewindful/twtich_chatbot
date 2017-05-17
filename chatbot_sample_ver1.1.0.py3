import socket, string
import sys
from time import sleep
import random
import requests
import time

 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "chatbot_name" #chatbot
MAIN_CAHTROOM = "join_chatroom" #join room
PORT = 6667
#http://www.twitchapps.com/tmi/
#login chatbot account and copy pass and replace it
PASS = "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
readbuffer = ""
#MODT = True
MODT = False
SLOW_CHAT_TIME = 1
ChatJoin_OnOff = 0 # 1 = chatjoin On , 0 = chatjoin Off

#usersname = "icewindful" #use get channel infomation.
usersname = "join_channel" 
get_info = "channels"
#how to get client_localhost
#https://dev.twitch.tv/docs/v5/guides/using-the-twitch-api
#Name : linkName
#Redirect URI : http://localhost
#Application Category : ChatBot
#Register a developer application 
client_localhost = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user
def getMessage(line):
    separate = line.split(":", 2)
    message = separate[2]
    return message
 
FaceWord = ["ヾ(*´∀ ˋ*)ﾉ", "(｢･ω･)｢", "(灬ºωº灬)",
            "｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡", "(๑•̀ω•́)ノ", "(っ●ω●)っ",
            "✧*｡٩(ˊᗜˋ*)و✧*｡", "(๑•̀ㅂ•́)و✧", "ฅ●ω●ฅ", 
            "(ΦωΦ)","─=≡Σ((( つ•̀ω•́)つ","ก็ʕ•͡ᴥ•ʔ ก้"]

ModUser = ["icewind1","icewind2","icewind3","icewind4","icewind5"]
JoinPass = ["icewind1","icewind2","icewind3","icewind4","icewind5","kimikobot","curseappbot","nightbot"]

#print("face_word_len")
#print(len(face_word))

#this get channel infomation. ex:follows , etc.
r_follow_info = requests.get('https://api.twitch.tv/kraken/' + get_info + '/' + usersname + "/follows"+ '?client_id=' + client_localhost)

followNowTotal = r_follow_info.json()["_total"]
print("now_follower_total")
print(followNowTotal)

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + MAIN_CAHTROOM + " \r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
#s.send("PASS " + PASS + "\r\n")
#s.send("NICK " + NICK + "\r\n")
#s.send("JOIN #icewindful \r\n")
 
# Method for sending a message
def Send_message(message):
    #s.send(bytes("PRIVMSG #" + MAIN_CAHTROOM + " :" + message + "\r\n").encode("UTF-8"))
    s.send(bytes("PRIVMSG #" + MAIN_CAHTROOM + " :" + message + "\r\n", "UTF-8"))

 
while True:
    sleep(1.00)
    r_follow_info = requests.get('https://api.twitch.tv/kraken/' + get_info + '/' + usersname + "/follows"+ '?client_id=' + client_localhost)
    #readbuffer = readbuffer + s.recv(1024).decode("UTF-8") 
    readbuffer = readbuffer + s.recv(2048).decode() 
    #temp = string.split(readbuffer, "\n")
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    new_follow = r_follow_info.json()["_total"]

    #new follows speak
    if(followNowTotal < new_follow):
        Send_message("【ICE】感謝" + r_follow_info.json()['follows'][0]['user']['display_name'] +"追隨!!,Thanks you follow!!)" "\r\n")
    
    followNowTotal = new_follow

    for line in temp:
        #fix cp950 windosw decode issues
        print (line.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
        #print(line.encode().decode('cp950'))
        if "PING" in line:
            #s.send(bytes((line.replace("PING", "PONG")),"UTF-8"))
            #break
            #s.send(bytes("PONG :pingis\r\n"), "UTF-8"))
            #break
            s.send(bytes(("PONG %s\r\n" % line[1]), "UTF-8"))
            break  
        elif("JOIN" in line):
            #print("======  JOIN ======")
            join_split = str.split(line, "!")
            #print(join_split[0])
            join_name =  str.split(join_split[0], ":")
            print(join_name[1])
            JoinUser = join_name[1]

            for JoinUser in JoinPass :
                print("")
            else:
                r_initial = requests.get('https://api.twitch.tv/kraken/users/' + join_name[1] + '?client_id=' + client_localhost)
                #Send_message("" + face_word[random.randrange(0,(len(face_word)),1)] + "歡迎 " + join_name[1] +" 參觀【ICE】的實況 \r\n")
                if(ChatJoin_OnOff == 1):
                    Send_message("" + FaceWord[random.randrange(0,(len(face_word)),1)] + "歡迎 " + r_initial.json()['display_name'] +" 參觀【ICE】的實況 \r\n")

            #print("======  END  ======")
        else:
            # Splits the given string so we can work with it better
            parts = str.split(line, ":")
 
            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                try:
                    # Sets the message variable to the actual message sent
                    message = parts[2][:len(parts[2]) - 1]
                except:
                    message = ""
                # Sets the username variable to the actual username
                usernamesplit = str.split(parts[1], "!")
                username = usernamesplit[0]
               
                # Only works after twitch is done announcing stuff (MODT = Message of the day)
                if MODT:
                    print (username + ": " + message)
                    '''
                    if (((message.upper() == "hi".upper())) & (len(message) == 2) ):
                        Send_message("Welcome to icewindful stream \r\n")
                        sleep(SLOW_CHAT_TIME)
                        break
                    if ((message.upper() == "Hello".upper()) & (len(message) == 5)):
                        Send_message("Hello "+ username + ", ICE chatbot. \r\n")
                        sleep(SLOW_CHAT_TIME)
                        break
                    if (message == "!獵人評價"):
                        Send_message("【Twese】 孤高的堅持公會蟲棍S級獵人，求他用別武器的還不肯點頭!!")
                        sleep(5)
                        Send_message("【千石撫子】 輕弩與片手，各台亂入常玩魔物的S級獵人!!")
                        sleep(5)
                        Send_message("【艾爾】 神人級嘴巴，嘴砲S級獵人之尊!!")
                        sleep(5) 
                        Send_message("【尼馬】 很堅持男角與用生命加班的S級獵人!!")
                        sleep(5)
                        Send_message("【WWW】 TA網站有上榜的S級獵人高手，學技術找他!!")
                        sleep(5)
                        Send_message("【ICE】 略懂略懂型B級獵人，專業型醬油實況主!!")
                        break

                    if ((message == "安安") & (len(message) == 2)):
                        Send_message("你好阿!"+ username + ", 機器人向你問安 \r\n")
                        sleep(SLOW_CHAT_TIME)
                        break
                    if ((message == "安") & (len(message) == 1)):
                        Send_message("你好阿!"+ username + ", 機器人向你問安 \r\n")
                        sleep(SLOW_CHAT_TIME)
                        break
                    '''
                    #print (len(message))
                    # You can add all your plain commands here
                    for username in ModUser :
                        if message == "!chatbot_close":
                            exit()
                        if message == "!slow_mod":
                            SLOW_CHAT_TIME = 3
                            break
                        if message == "!nor_mod":
                            SLOW_CHAT_TIME = 1
                            break
                        if message == "!join_msg_on":
                            ChatJoin_OnOff = 1
                            Send_message("聊天室加入頻道訊息 ON\r\n")
                            break
                        if message == "!join_msg_off":
                            ChatJoin_OnOff = 0
                            Send_message("聊天室加入頻道訊息 OFF\r\n")
                            break

                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True 


                    

                

