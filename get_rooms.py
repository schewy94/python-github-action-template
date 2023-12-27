import os
import telebot
import requests
import pandas as pd

API_Key = "6453714074:AAEJFCtoIRzxkBtoKF1H2ExlGz-IvgaSUoc"
bot = telebot.TeleBot(API_Key )

# print("going")

# @bot.message_handler(commands=['checkroom'])

# def greet(message):
#     # range 1 - 3
number_of_people = 1

def get_room_inventory(arrangement_id):
    # Define the API URL
    url = f"https://rwcruises.partner.flickket.com/v1/usrcsrv/arrangements/{arrangement_id}/units?translation=false&preview=0"

    # Make the HTTP request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        inventories = data["result"]["inventories"]

        # Initialize inventory values
        balcony_stateroom_inventory = 0
        balcony_deluxe_stateroom_inventory = 0

        # Find the inventory for "Balcony Stateroom" and "Balcony Deluxe Stateroom"
        for price in data["result"]["prices"]:
            # print(price)
            if price["name"] == "Balcony Stateroom":
                inventory_id = str(price["inventory_id"])
                if inventory_id in inventories:
                    balcony_stateroom_inventory = inventories[inventory_id]
            elif price["name"] == "Balcony Deluxe Stateroom":
                inventory_id = str(price["inventory_id"])
                if inventory_id in inventories:
                    balcony_deluxe_stateroom_inventory = inventories[inventory_id]
                # print(inventories[inventory_id])

        # Create a dictionary with the inventory values
        # room_inventory = {
        #     "Balcony Stateroom": balcony_stateroom_inventory,
        #     "Balcony Deluxe Stateroom": balcony_deluxe_stateroom_inventory
        # }
        # print(room_inventory)
        return f'Bal : {balcony_stateroom_inventory} | Bal Del {balcony_deluxe_stateroom_inventory}'

    else:
        print(f"Failed to retrieve data for Arrangement ID {arrangement_id}. Status code: {response.status_code}")
        return None

phucket_dict = {
    1 : 319833,
    2 : 319837,
    3 : 319840
}
penang_dict = {
    1: 319797,
    2: 319801,
    3: 319821,
}

friday_dict={
    1:319760
}

wednesday_dict={
    1:319744
}

loc_dict = {
    "Penang" : penang_dict,
    "Phucket": phucket_dict,
    "Wednesday": wednesday_dict,
    "Friday" : friday_dict
}
res = ""
for i in ["Penang","Phucket","Wednesday","Friday"]:
    package_id = loc_dict[i][number_of_people]

    url = f'https://rwcruises.partner.flickket.com/v1/experiencesrv/packages/schedule_service/get_schedules_and_units?translation=false&package_id={package_id}&preview=0'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    res += f'{i}\n'

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # print(data["result"]["schedules"])
        for item in data["result"]["schedules"]:
            res += f'{item["date"]} : {get_room_inventory(item["time_slots"][0]["arrangement_id"])}\n'


send_url = 'https://api.telegram.org/bot6453714074:AAEJFCtoIRzxkBtoKF1H2ExlGz-IvgaSUoc/sendmessage?chat_id=-4067239998&text="{}"'.format(res)
# print(send_url)
requests.get(send_url)
print("sent")
