from WhereToMeetbot import WhereToMeet_bot
from getDistance import * 
import csv
import pandas as pd
import telegram

START_CMD = "/start@WhereToMeetBot"
JOIN_CMD = "/join@WhereToMeetBot"
GO_CMD = "/go@WhereToMeetBot"


update_id = None

# initialises the WhereToMeet_bot class
bot = WhereToMeet_bot("config.cfg")

# read CSV file
# bbt_locations = pd.read_csv('BBTgeocodes.csv')

# filter_list = []
# filter_dict = {}

group_dict = {}
user_dict = {}

df = pd.read_csv('mrt.csv')

def make_reply(msg):
    if msg is not None:
        reply = msg
    return reply

while True:
    print("...")
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]

    if updates:
        for item in updates:
            update_id = item["update_id"]
            message = None
            # longi = None
            # lati = None
            # location_list = []
            print(item)
            # get message text
            try:
                # extract out the text sent to bot
                message = item["message"]["text"]
            except:
                pass

            try:
                message_type = item["message"]["chat"]["type"]
            except:
                continue

            try:
                test = item["message"]
            except:
                continue

            # check if from group
            if item["message"]["chat"]["type"] == "supergroup":
                group_id = item["message"]["chat"]["id"]
                # check if is "/start"
                if message == START_CMD:
                    if group_id not in group_dict.keys():
                        bot.send_message("WhereToMeet bot will help you calculate the nearest MRT. Send /join to join!", group_id)
                        group_dict[group_id] = {}
                    else:
                        bot.send_message("You already started!", group_id)
    

                # Join messages from a group that has started
                if group_id in group_dict.keys() and message == JOIN_CMD:
                    print("join!")
                    user_id = item["message"]["from"]["id"]
                    user_name = item["message"]["from"]["username"]
                    group_dict[group_id][user_id] = None
                    if user_id not in user_dict.keys():
                        user_dict[user_id] = {}
                        user_dict[user_id]["name"] = user_name
                        user_dict[user_id]["groups"] = [group_id]
                    else:
                        user_dict[user_id]["groups"].append(group_id)
                    location_keyboard = telegram.KeyboardButton(text = "Send my location", request_location=True)
                    custom_keyboard = [[location_keyboard]]
                    reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
                    bot.bot.send_message(text="Please send your location", chat_id=user_id, reply_markup=reply_markup)

                # Go
                if group_id in group_dict.keys() and message == GO_CMD:
                    no_location_users = []
                    for user, location in group_dict[group_id].items():
                        if location == None:
                            no_location_users.append(user)
                    

                    # if all users have sent then is a go
                    if not no_location_users:
                        bot.send_message("Calculating location!!", group_id)
                        # calculate distance
                        mrt_locations = getTopKClosest(group_dict[group_id], df, 3)
                        text_to_send = "Closest 3 locations\n"
                        for location in mrt_locations:
                            text_to_send += location + "\n"
                        text_to_send.rstrip()
                        bot.send_message(text_to_send, group_id)

                        # clean up user and group
                        
                        users = group_dict.pop(group_id, None)
                        for user in users:
                            groups = user_dict[user]["groups"]
                            groups.remove(group_id)
                            if not groups:
                                user_dict.pop(user, None)
                            

                    else:
                        text_to_send = "These users have not sent their location.\n"
                        for user in no_location_users:
                            text_to_send += "@" + user_dict[user]["name"] + "\n"
                        text_to_send.rstrip()
                        bot.send_message(text_to_send, group_id)

            # for PMs
            if item["message"]["chat"]["type"] == "private":
                user_id = item["message"]["from"]["id"]
                print("debug1")
                longi = None
                lati = None
                try:
                # extract out longitude and latitude
                    longi = item["message"]["location"]["longitude"]
                    lati = item["message"]["location"]["latitude"]
                except:
                    pass
                # if location message
                if longi is not None and lati is not None :
                    # Add location to all groups this user belongs to
                    for group in user_dict[user_id]["groups"]:
                        print("assigning location")
                        group_dict[group][user_id] = (lati, longi)

            
            # try:
            #     # extract out longitude and latitude
            #     longi = item["message"]["location"]["longitude"]
            #     lati = item["message"]["location"]["latitude"]
            # except:
            #     pass

            # try:
            #     from_ = item["message"]["from"]["id"]
            # except:
            #     from_ = item["edited_message"]["from"]["id"]

            # try: 
            #     username = item["message"]["from"]["username"]
            # except:
            #     username = "unknown"

            # print(message)
            # print(username)
            # bot.send_message("hi sg", 130584658)
            
            # if from_ in filter_dict.keys() and lati is not None and longi is not None:
            #     brand = filter_dict.pop(from_)
            #     location_list = getTopBrand(lati, longi, bbt_locations, 3, brand)
            #     for i in range(len(location_list)):
            #         bot.bot.sendMessage(chat_id=from_, text=str(i + 1) + ". " + location_list[i])
            #     start_keyboard = telegram.KeyboardButton(text="return")
            #     custom_keyboard = [[start_keyboard]]
            #     reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
            #     bot.bot.sendMessage(chat_id=from_, text="Return to main menu", reply_markup=reply_markup)

            # elif message == "/start" or message == "return":
            #     # trigger a button to send location
            #     location_keyboard = telegram.KeyboardButton(text="Find me BBT!🍵", request_location=True)
            #     brand_keyboard = telegram.KeyboardButton(text="Filter by brand!")
            #     custom_keyboard = [[location_keyboard],[brand_keyboard]]
            #     reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
            #     bot.bot.sendMessage(chat_id=from_, text="Welcome to WhereToBBT!", reply_markup=reply_markup)
            
            # elif message == "Filter by brand!":
            #     # list brands
            #     filter_list.append(from_)
            #     koi_keyboard = telegram.KeyboardButton(text="Koi")
            #     gongcha_keyboard = telegram.KeyboardButton(text="Gong Cha")
            #     liho_keyboard = telegram.KeyboardButton(text="LiHo")
            #     playmade_keyboard = telegram.KeyboardButton(text="Playmade")
            #     heytea_keyboard = telegram.KeyboardButton(text="HeyTea")
            #     tigersugar_keyboard = telegram.KeyboardButton(text="Tiger Sugar")
            #     rnb_keyboard = telegram.KeyboardButton(text="R&B Tea")
            #     xingfutang_keyboard = telegram.KeyboardButton(text="Xing Fu Tang")
            #     partea_keyboard = telegram.KeyboardButton(text="PARTEA")
            #     teatreecafe_keyboard = telegram.KeyboardButton(text="Tea Tree Cafe")
            #     brands_keyboard = [[gongcha_keyboard],[koi_keyboard],[liho_keyboard],[playmade_keyboard],[rnb_keyboard],[teatreecafe_keyboard],[tigersugar_keyboard],[xingfutang_keyboard]]
            #     reply_markup = telegram.ReplyKeyboardMarkup(keyboard=brands_keyboard, resize_keyboard=True, one_time_keyboard=True)
            #     bot.bot.sendMessage(chat_id=from_, text="Choose your brand!", reply_markup=reply_markup)
                
            # elif message is not None and from_ in filter_list:
            #     filter_list.remove(from_)
            #     filter_dict[from_] = message
            #     location_keyboard = telegram.KeyboardButton(text="BBT me now!", request_location=True)
            #     custom_keyboard = [[location_keyboard]]
            #     reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
            #     bot.bot.sendMessage(chat_id=from_, text="Send your location", reply_markup=reply_markup)
                
            # # net to catch random messages
            # elif message is not None:
            #     # prompts user to /search
            #     reply = make_reply("Please enter '/start' to start search")
            #     bot.send_message(reply, from_)

            # # user clicks find me bubble tea
            # elif longi is not None and lati is not None :
            #     location_list =  getTopKClosest(lati, longi, bbt_locations, 3)
            #     for i in range(len(location_list)):
            #         bot.bot.sendMessage(chat_id=from_, text=str(i + 1) + ". " + location_list[i])
            # else:
            #     pass

