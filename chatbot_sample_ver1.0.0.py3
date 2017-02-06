import socket, string
import sys
from time import sleep

#it run python 3.5 version
#https://www.twitch.tv/icewindful
#is is my twitch live bot sample code
#if you like it follow me,thanks
 
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "twitchbot_account"
MAIN_CAHTROOM = "chat_room_account"
PORT = 6667
#http://www.twitchapps.com/tmi/
#login chatbot account and copy pass and replace it
#example oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 
PASS = "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
readbuffer = ""
#MODT = True
MODT = False
SLOW_CHAT_TIME = 1

def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user
def getMessage(line):
    separate = line.split(":", 2)
    message = separate[2]
    return message
 
# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + MAIN_CAHTROOM + " \r\n", "UTF-8"))
#get chatroom member list.
s.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
 
# Method for sending a message
def Send_message(message):
    #s.send(bytes("PRIVMSG #" + MAIN_CAHTROOM + " :" + message + "\r\n").encode("UTF-8"))
    s.send(bytes("PRIVMSG #" + MAIN_CAHTROOM + " :" + message + "\r\n", "UTF-8"))

while True:
    #readbuffer = readbuffer + s.recv(1024).decode("UTF-8") 
    readbuffer = readbuffer + s.recv(2048).decode() 
    #temp = string.split(readbuffer, "\n")
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        #fix cp950 windosw decode issues
        print (line.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding))
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

            #have a viewer join chat romm is show how join.
            print(join_name[1])
            #if not show name join it.
            if((join_name[1] == "nightbot") | (join_name[1] == "curseappbot")):
                print("")
            else:
                Send_message("Welcome" + join_name[1] +" my live \r\n")
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
                    #print (len(message))
                    # You can add all your plain commands here
                    if (((message.upper() == "hi".upper())) & (len(message) == 2) ):
                        Send_message("Welcome to icewindful stream \r\n")
                        sleep(SLOW_CHAT_TIME)
                        break
                    if ((message.upper() == "Hello".upper()) & (len(message) == 5)):
                        Send_message("Hello "+ username + ", My is chatbot. \r\n")
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

                    #if exit it you can chatroom enter !chatbot_close
                    if message == "!chatbot_close":
                            exit()
                        
                for l in parts:
                    if "End of /NAMES list" in l:
                        MODT = True 

