import requests

def check_balcony_stateroom_availability(id):
    # Define the API URL
    url = f'https://rwcruises.partner.flickket.com/v1/usrcsrv/arrangements/{id}/units?translation=false&preview=0'

    # Make the HTTP request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
    
        # Get the inventory data
        inventory_data = data["result"]["inventories"]
        message = ""
        # Loop through the prices and check if the inventory is available
        for price in data["result"]["prices"]:
            if price["name"] != "Port Charge (per pax)":
                inventory_id = str(price["inventory_id"])
                name = price["name"]
                # Check if the inventory is available
                if inventory_id in inventory_data and inventory_data[inventory_id] > 0:
                    message += f"Name: {name}, Inventory Available: {inventory_data[inventory_id]}\n"
                
        # Find the "Balcony Stateroom" object and get its inventory ID
        balcony_stateroom = next((room for room in data["result"]["prices"] if room["name"] == "Balcony Stateroom" or room["name"] == "Balcony Deluxe Stateroom"), None)
        if balcony_stateroom:
            inventory_id = balcony_stateroom.get("inventory_id")
            
            # Check the inventory in the inventories object
            if inventory_id and data["result"]["inventories"].get(str(inventory_id)) > 1:
                # print("Balcony Stateroom is available with inventory greater than 1.")
                message += "Balcony available"
                send_url = 'https://api.telegram.org/bot6453714074:AAEJFCtoIRzxkBtoKF1H2ExlGz-IvgaSUoc/sendmessage?chat_id=1607046133&text={}'.format(message)
                requests.get(send_url)
                print(message)
                # print("Balcony Stateroom is not available")
        else:
            print("Balcony Stateroom not found in the response.")

# Run the code every four hours
arrangement_id = 1709424000319833# 3/3

roomtype = "Balcony Stateroom"
# arrangement_id = 1708041600319760 #16/2 Friday

check_balcony_stateroom_availability(arrangement_id)
