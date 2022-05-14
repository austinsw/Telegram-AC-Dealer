from telegram.ext import Updater  # pip3 install python-telegram-bot --upgrade
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
from telegram import ParseMode
import requests
import time
from threading import Thread

BOT_TOKEN = "1120654321:AC-DeaLeR_bOt-TokeN" ### ac_dealer Bot
sim_token = 'esfshgfgd.FiveSim.toKen-fefs3412dvgdf' # 5sim api token
country = 'canada'
operator = 'any'
product = 'telegram'
headers = {
    'Authorization': 'Bearer ' + sim_token,
    'Content-Type': 'application/json',
}

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

###### Initialization1 ######
users = [1234567666, 1234567555]    # User1, User2
users_num = [5,5]
super_users = [1772021543, 1772022321, 1772021123]  # Admins' id / usernames
def listToFile(fileName, ls):
    with open(fileName, 'w') as filehandle:
        filehandle.writelines("%s," % data for data in ls)

def fileToList(fileName, ls):
    with open(fileName, 'r') as filehandle:
        a = filehandle.read()
    a = a.split(',')
    a.pop()
    b = []
    for element in a:
        try:
            b.append(int(element))
        except:
            b.append(element)
    return b

"""listToFile("users.txt", users)           ###### Initialization2 ######
listToFile("users_num.txt", users_num)
listToFile("super_users.txt", super_users)"""
users = fileToList("users.txt", users)
users_num = fileToList("users_num.txt", users_num)
super_users = fileToList("super_users.txt", super_users)
print(users)
print(users_num)
print(super_users)

def index(ID, L):
    try:
        return(L.index(ID))
    except:
        return -1

def updateNum(ID, num):
    try:
        ID = int(ID)
    except:
        pass
    pos = index(ID, users)
    if pos != -1:
        users_num[pos] += num
        attempts = users_num[pos]
        print(users)  ###
        print(users_num)  ###
        if users_num[pos] < 1:
            print("users num < 1, gets deleting") ###
            del users[pos]
            del users_num[pos]
            attempts = 0
            print(users)    ###
            print(users_num)    ###
    else:
        users.append(ID)
        users_num.append(num)
        attempts = users_num[-1]
    listToFile("users.txt", users)
    listToFile("users_num.txt", users_num)
    return attempts

def showUsers():
    msg = []
    for i in range(len(users)):
        msg.append([users[i],users_num[i]])
    return msg

def makePurchase():  ############
    response = requests.get('https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + product,
                            headers=headers)
    id = str(response.json()['id'])
    phone = response.json()['phone']
    return id, phone

def checkSMS(ID):  ############
    for number in range(36):    ### Total of 3m
        time.sleep(5)
        try:
            response = requests.get('https://5sim.net/v1/user/check/' + ID, headers=headers)
            code = response.json()['sms'][0]['code']
            print(ID, "got the code", code)
            return code
        except:
            print(ID,"waited", number*5, "seconds")
    print(ID,"Failed to get the code...")
    return

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ID: " + str(update.effective_chat.id))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

def add(update, context):
    print("Adding start:") ###
    pos = index(update.effective_chat.id, super_users)
    if pos == -1:
        pos = index(update.effective_chat.username, super_users)
    if pos != -1:
        try:  # Takes 2 arguements
            userID, num = context.args
            try:
                attempts = updateNum(userID, int(num))
                context.bot.send_message(chat_id=update.effective_chat.id, text=str(userID) + " updated. Attempts = " + str(attempts))
                print(users)  ###
                print(users_num)  ###
            except:
                print("Input arguments, wrong format")  ###
                print(users)  ###
                print(users_num)  ###
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Incorrect format. \nTry /add [username/ID] [No. of attempts]")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Incorrect format. \nTry /add [username/ID] [No. of attempts]")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unauthorized.")

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)

def buy_and_check(update, context):
    pos = index(update.effective_chat.id, users)
    if pos != -1:
        #updateNum(update.effective_chat.id, -1)
        found = update.effective_chat.id
        print(update.effective_chat.id,"verified")
    else:
        pos = index(update.effective_chat.username, users)
        if pos != -1:
            #updateNum(update.effective_chat.username, -1)
            found = update.effective_chat.username
            print(update.effective_chat.username,"verified")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Unauthorized. Ask supervisor to give you more number of attempts.")
            return
    print("pos!=-1")
    try:
        purChaseID, phoneNo = makePurchase()
        msg = "Order id: " + str(purChaseID) + "\nHow to gain access to the account: \n1. Use " + phoneNo + " to create account on TelegramX (Android)/Nicegram (IOS). \n2. After signing in with the number, click next. \n3. The sms code will be sent to you shortly. \n(4. If the code is not here after 3 minutes, try /request again.)"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        code = checkSMS(purChaseID)
        try:
            context.bot.send_message(chat_id=update.effective_chat.id, text=code)
            updateNum(found, -1)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Order: " + str(purChaseID) + " failed.")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to purchase.")

def request(update, context):
    thr = Thread(target=buy_and_check, args=[update,context])
    thr.start()

request_handler = CommandHandler('request', request)
dispatcher.add_handler(request_handler)


def user(update, context):
    print(update.effective_chat.id) ###
    pos = index(update.effective_chat.id, super_users)
    if pos == -1:
        pos = index(update.effective_chat.username, super_users) ########################
    if pos != -1:
        userID = ' '.join(context.args)
        try:
            userID = int(userID)
        except:
            pass
        idx = index(userID, users)
        print(idx)  ###
        print(users_num[idx])
        if idx != -1:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Number of remaining attempts: " + str(users_num[idx]))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="User does not exist.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unauthorized.")

user_handler = CommandHandler('user', user)
dispatcher.add_handler(user_handler)


def list(update, context):
    pos = index(update.effective_chat.id, super_users)
    if pos == -1:
        pos = index(update.effective_chat.username, super_users)
    if pos != -1:
        message = showUsers()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Unauthorized.")

list_handler = CommandHandler('list', list)
dispatcher.add_handler(list_handler)


def help(update, context):
    message = "/request \n/add [user_id] [num] \n/list \n/user [user_id]"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)