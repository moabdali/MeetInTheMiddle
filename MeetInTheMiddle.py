import PySimpleGUI as psGUI             #making the popups and window
from geopy.geocoders import Nominatim   #geolocation use pip install geopy
import webbrowser                       #open google maps
import sys


#initialize geolocator
geolocator = Nominatim(user_agent="MeetInTheMiddle")

psGUI.theme('DarkAmber')   # Add a little color to the window

#Makes sure your initial inputs are legal
def numCarsErrorCheck(numOfCars):
    # clean exit if no cars are entered or if exited/cancelled
    if not numOfCars:
        psGUI.popup_cancel('User has decided to exit.')
        sys.exit()
    # check to make sure a number was entered
    
    try:
        int(numOfCars)
    except ValueError:
        psGUI.popup_cancel('You must type in a positive integer.')
        return 1
    # check to make sure it was positive
    if int(numOfCars) < 1:
        psGUI.popup_cancel('You must type in a positive integer.')
        return 2
    return 0

friendArray = []

# will determine the number of addresses you can input later

carNumLayout = [[psGUI.Text("How many cars will be going to the meet up location?")]]
carNumLayout.append( [psGUI.T("Number of cars: "), psGUI.InputText()])
carNumLayout.append( [psGUI.Button('Submit')] )
carNumWindow = psGUI.Window('CarNumWindow', carNumLayout)

while True:
    event,values = carNumWindow.read()
    if event == 'Submit':
        numOfCars = values[0]
        result = numCarsErrorCheck(numOfCars)
        if result == 0:
            carNumWindow.close()
            break
        else:
            continue
numOfCars = int(numOfCars)


#create the window
layout = [[psGUI.Text('Enter each person\'s address below.  Use at least street,city and state.')]]
for i in range(int(numOfCars)):
    layout.append( [psGUI.T("Address "+str(i+1),size = (10,1)), psGUI.InputText(key=i)])
layout.append( [psGUI.Button('Calculate')] )
meetInMiddle = psGUI.Window('Meet in Middle', layout)


while True:
    event, values = meetInMiddle.read()
    if event == 'Quit' or event == psGUI.WIN_CLOSED:
        sys.exit()

    if event == 'Calculate':
        for i in values:
            location =(geolocator.geocode(values[i]))
            print(location)
            friendArray.append((location.latitude, location.longitude))

    latiAverage = 0.0
    longAverage = 0.0

    #finds the average latlong of all the points (this is the central theme of this program!)
    for i in range (0,numOfCars):
        latiAverage = latiAverage + friendArray[i][0]
        longAverage = longAverage + friendArray[i][1]

    latiAverage = latiAverage / numOfCars
    longAverage = longAverage / numOfCars
    #averages out the lat long


    latLongAverage = (latiAverage,longAverage)
    #combine lat and long into one entry for easier usage


    #turn the latlong average into a real address (geopy attempts to use the closest address it can find)
    location = geolocator.reverse(latLongAverage)

    #close window
    break    

meetInMiddle.close()
layout1 = [
    [psGUI.Text('Your meet up address is :'+str(location.address)+"\n\nYou can click on Open Google below, and then NEARBY on the Google Maps page and then click RESTAURANTS or type\nPARKS to find somewhere to eat or hang out.\n")],
    [psGUI.Button("Open Google Maps"),psGUI.Button('Quit')]
    ]

openGoogle = psGUI.Window('Open Google', layout1)

while True:
    
    
    event = openGoogle.read()
    if event[0] == psGUI.WIN_CLOSED or event == 'Quit':
        openGoogle.close()
        sys.exit()
    if event[0] == "Open Google Maps":
        lookup = str(latLongAverage[0])+','+str(latLongAverage[1])
        openGoogle.close()
        webbrowser.open('https://www.google.com/maps/place/'+lookup)
        sys.exit()
        
    
    
