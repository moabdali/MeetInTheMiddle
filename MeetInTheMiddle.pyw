import PySimpleGUI as psGUI
from geopy.geocoders import Nominatim
import webbrowser
import sys

psGUI.theme('DarkAmber')   

# function to grab how many cars are meeting up
def get_num_of_cars():
    layout = [
        [psGUI.Text("How many cars will be going to the meetup location?")],
        [psGUI.Text("Number of cars: "), psGUI.InputText()],
        [psGUI.Button('Submit')]
    ]
    window = psGUI.Window('CarNumWindow', layout)

    while True:
        event, values = window.read()
        if event == 'Submit':
            num = values[0]
            result = num_cars_error_check(num)
            if result == 0:
                window.close()
                return int(num)
            else:
                continue
        if event == psGUI.WIN_CLOSED:
            window.close()
            sys.exit()

# function to error check the number of cars
def num_cars_error_check(num):
    if not num:
        psGUI.popup_cancel('User has decided to exit.')
        sys.exit()
    try:
        num = int(num)
    except ValueError:
        psGUI.popup_cancel('You must type in a positive integer.')
        return 1
    if num < 1:
        psGUI.popup_cancel('You must type in a positive integer.')
        return 2
    return 0

# function for getting addresses
def get_addresses(num_of_cars, default_texts):
    layout = [[psGUI.Text('Enter each person\'s address below. Use at least street, city, and state.')]]
    for i in range(num_of_cars):
        layout.append([
            psGUI.Text(f"Address {i+1}", size=(10, 1)), 
            psGUI.InputText(f'{default_texts[i]}', key=f"ADDR_{i}"),
            psGUI.Button('Clear', key=f"CLEAR_{i}")  # Add a clear button for each address
        ])
    layout.append([psGUI.Button('Calculate')])
    
    window = psGUI.Window('Meet in Middle', layout)
    
    while True:
        event, values = window.read()
        if event in (psGUI.WIN_CLOSED, 'Quit'):
            window.close()
            sys.exit()
        if event.startswith("CLEAR_"):
            addr_idx = int(event.split("_")[1])
            window[f"ADDR_{addr_idx}"].update("")
            default_texts[addr_idx] = ""
            continue
        if event == 'Calculate':
            coords = validate_addresses(values, default_texts)
            window.close()
            if coords:
                return coords

# make sure the addresses exist
def validate_addresses(addresses, default_texts):
    geolocator = Nominatim(user_agent="MeetInTheMiddle")
    valid_coordinates = []
    
    for i, addr_key in enumerate(addresses.keys()):
        addr = addresses[addr_key]
        location = geolocator.geocode(addr, timeout=1000000)
        default_texts[i] = addr
        
        if location:
            default_texts[i] = location
            valid_coordinates.append((location.latitude, location.longitude))
        else:
            psGUI.popup_error(f"Address {i+1}: {addr} is likely misspelled. Try again.")
            default_texts[i] = f"Address not found: {addr}"
            return
    return valid_coordinates

# calculate the balanced central location
def calculate_meetup_point(coordinates, num_of_cars):
    lat_sum = sum(coord[0] for coord in coordinates)
    lon_sum = sum(coord[1] for coord in coordinates)

    return lat_sum / num_of_cars, lon_sum / num_of_cars

# show the results
def display_final_window(meetup_location, default_texts):
    layout = [[psGUI.Text(f'Your meet up address is: {meetup_location}\nYou can click on "Open Google Maps" to view the location.')]]
    for i, addr in enumerate(default_texts):
        layout.append([psGUI.Text(f"Address {i+1}: {addr}")])
    layout.append([psGUI.Button("Open Google Maps"), psGUI.Button("Quit")])
    
    window = psGUI.Window('Open Google', layout)
    
    while True:
        event, _ = window.read()
        if event in (psGUI.WIN_CLOSED, 'Quit'):
            window.close()
            sys.exit()
        if event == "Open Google Maps":
            webbrowser.open(f'https://www.google.com/maps/place/{meetup_location}')
            window.close()
            sys.exit()

# main code here
def main():
    num_of_cars = get_num_of_cars()
    default_texts = [""] * num_of_cars
    
    while True:
        coordinates = get_addresses(num_of_cars, default_texts)
        if not coordinates:
            continue
        
        meetup_location = calculate_meetup_point(coordinates, num_of_cars)
        geolocator = Nominatim(user_agent="MeetInTheMiddle")
        meetup_address = geolocator.reverse(meetup_location).address
        if display_final_window(meetup_address, default_texts):
            continue
        else:
            break

# Python shenanigans in case someone tries to import this as a module (why would you,though?!)
if __name__ == "__main__":
    main()
