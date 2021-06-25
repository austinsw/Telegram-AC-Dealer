from telegram.ext import Updater  # pip3 install python-telegram-bot --upgrade
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import requests
import time

BOT_TOKEN = "***********" ###Bot
sim_token = '********************************************' #5sim token
country = 'philippines'
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

###### Initialization ######
users = [***, ***]    #Kelvin, Sawyer id
users_num = [5,5]
super_users = [******, ******, ******, ******, ******]  #People's id


def listToFile(fileName, ls):
    with open(fileName, 'w') as filehandle:
        filehandle.writelines("%s " % data for data in ls)

def fileToList(fileName, ls):
    with open(fileName, 'r') as filehandle:
        a = filehandle.read()
    a = a.split(',')
    a.remove(' ')
    b = []
    for element in a:
        b.append(int(element))
    return b

"""listToFile("users.txt", users)           ###### Initialization ######
listToFile("users_num.txt", users_num)
listToFile("super_users.txt", super_users)
fileToList("users.txt", users)
fileToList("users_num.txt", users_num)
fileToList("super_users.txt", super_users)
print(users)
print(users_num)
print(super_users)"""

def index(ID, L):
    try:
        return(L.index(ID))
    except:
        return -1

def updateNum(ID, num):
    pos = index(ID, users)
    if pos != -1:
        users_num[pos] += num
        print(users)  ###
        print(users_num)  ###
        if users_num[pos] < 1:
            print("users num < 1, gets deleting") ###
            del users[pos]
            del users_num[pos]
            print(users)    ###
            print(users_num)    ###
    else:
        users.append(ID)
        users_num.append(num)
    listToFile("users.txt", users)
    listToFile("users_num.txt", users_num)

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
            return response.json()['sms'][0]['code']
            break
        except:
            print("waited 5s~")
    return "Failed to get the code..."

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

def add(update, context):
    print("see if something goes wrong") ###
    pos = index(update.effective_chat.id, super_users)
    if pos != -1:
        try:  # Takes 2 arguements
            userID, num = context.args
            try:
                updateNum(int(userID), int(num))
                context.bot.send_message(chat_id=update.effective_chat.id, text="User updated.")
                print(users)  ###
                print(users_num)  ###
            except:
                print("Input arguments, wrong format")  ###
                print(users)  ###
                print(users_num)  ###
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="An error has occured. Please check the format of your command.")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="An error has occured. Please check the format of your command.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized for this action.")

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)


def request(update, context):
    #print(update.effective_chat.id) ###
    #print(type(update.effective_chat.id))  ###
    pos = index(update.effective_chat.id, users)
    if pos != -1:
        updateNum(update.effective_chat.id, -1)
        try:
            purChaseID, phoneNo = makePurchase()
            message = "Here is the phone no. you requested: " + phoneNo + ". Please try logging in and the sms code will be sent to you shortly."
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            code = checkSMS(purChaseID)
            context.bot.send_message(chat_id=update.effective_chat.id, text=code)
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to make purchase.....")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized for this action.")

request_handler = CommandHandler('request', request)
dispatcher.add_handler(request_handler)


def user(update, context):
    print(update.effective_chat.id) ###
    pos = index(update.effective_chat.id, super_users)
    if pos != -1:
        userID = ' '.join(context.args)
        print(userID) ###
        print(type(userID)) ###
        try:    ############################################################
            idx = index(int(userID), users)
            print(idx)  ###
            print(users_num[idx])
            if idx != -1:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Number of remaining applications: " + str(users_num[idx]))
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="User does not exist.")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="UserID needs to be an integer.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized for this action.")

user_handler = CommandHandler('user', user)
dispatcher.add_handler(user_handler)


def list(update, context):
    pos = index(update.effective_chat.id, super_users)
    if pos != -1:
        message = showUsers()
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized for this action.")

list_handler = CommandHandler('list', list)
dispatcher.add_handler(list_handler)


def help(update, context):
    message = "/request \n/add {user_id} {num} \n/list \n/user {user_id}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
