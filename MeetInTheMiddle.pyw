import PySimpleGUI as psGUI             #making the popups and window
from geopy.geocoders import Nominatim   #geolocation use pip install geopy
import webbrowser                       #open google maps
import sys


#initialize geolocator
geolocator = Nominatim(user_agent="MeetInTheMiddle")

# Add a little color to the windows
psGUI.theme('DarkAmber')   

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


# the array that keeps track of the address longlats
friendArray = []

# will determine the number of addresses you can input later
carNumLayout = [[psGUI.Text("How many cars will be going to the meet up location?")]]
carNumLayout.append( [psGUI.T("Number of cars: "), psGUI.InputText()])
carNumLayout.append( [psGUI.Button('Submit')] )
carNumWindow = psGUI.Window('CarNumWindow', carNumLayout)
#makes sure the numbers are valid
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

#this will keep track of the user's input so that they don't have to keep reentering it
#if there's an error that makes them revisit the address entry screen.  Starts out blank
defaultText = []
for i in range(0,numOfCars):
    defaultText.append("")


# get addresses from user
while True:
    # flag for assuming the user hasn't put in a good address yet
    errorSpelling = False
    
    #create the window
    layout = [[psGUI.Text('Enter each person\'s address below.  Use at least street,city and state.')]]
    for i in range(int(numOfCars)):
        layout.append( [   psGUI.T("Address "+str(i+1),size = (10,1)), psGUI.InputText(f'{defaultText[i]}',key=i) ])
    layout.append( [psGUI.Button('Calculate'),psGUI.Button('Clear')])
    meetInMiddle = psGUI.Window('Meet in Middle', layout)

    # get inputs
    event, values = meetInMiddle.read()

    # if they want to clear an input
    if event == 'Clear':
        for i in range(0,numOfCars):
            defaultText[i] = values[i]
        meetInMiddle.close()
        while True:
            getNum = psGUI.popup_get_text("Which address would you like to clear out?", default_text="1")
            try:
                getNum = int(getNum)
            except:
                print("That's not a number.  Try again.")
                continue
            if getNum <1 or getNum >numOfCars:
                print("That's an invalid address.")
                continue
            else:
                defaultText[getNum-1] = ""
                break
        continue
    
    #quit    
    elif event == 'Quit' or event == psGUI.WIN_CLOSED:
        sys.exit()
    
    #user attempts to calculate central location; program will validate addresses and throw an error if it can't find one of the addresses
    elif event == 'Calculate':
        for i in values:
            meetInMiddle.close()
            location =(geolocator.geocode(values[i], timeout = 1000000))
            defaultText[i] = values[i]
            # for successful lookups (i.e. location isn't saved as a None), replace the addresses with more detailed addresses that were returned by the API
            if location != None:
                defaultText[i] = location
                
            #if an error occurs, it means an address wasn't found; this exception handling allows the user to try again
            try:
                friendArray.append((location.latitude, location.longitude))

            except AttributeError:
                meetInMiddle.close()
                psGUI.popup(f"An error occurred: Address {i+1}:  [{values[i]}] is likely misspelled.  Try again.")
                defaultText[i] = f"Address not found: "+f"{defaultText[i]}"
                errorSpelling = True
    # if the previous error checks passed, then the program may proceed; otherwise it goes back to the text entry until a valid input is received
    if errorSpelling == True:
        continue
    
    #close the window to avoid duplicates
    meetInMiddle.close()
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


    # creates the final window; shows the calculated central location and shows detailed information on the addresses the program found; if the user feels an incorrect address was found, they can try again
    layout1 = []
    layout1.append( [ psGUI.Text('Your meet up address is: '+str(location.address)+"\n\nYou can click on Open Google below, and then NEARBY on the Google Maps page and then click RESTAURANTS or type\nPARKS to find somewhere to eat or hang out.\n")])
    for i in range(0,numOfCars):
        layout1.append( [psGUI.Text(f"Address {i+1}: {defaultText[i]}")])
    layout1.append([psGUI.Button("Open Google Maps"), psGUI.Button("Change addresses"),psGUI.Button("Quit")])
    openGoogle = psGUI.Window('Open Google', layout1)

    print(defaultText)
    
    # user may exit, open google maps, or change their addresses (in case they used insufficient info and an incorrect city/state was found)
    while True:
        event = openGoogle.read()
        if event[0] == psGUI.WIN_CLOSED or event[0] == 'Quit':
            meetInMiddle.close()
            openGoogle.close()
            sys.exit()
        if event[0] == "Open Google Maps":
            lookup = str(latLongAverage[0])+','+str(latLongAverage[1])
            meetInMiddle.close()
            openGoogle.close()
            webbrowser.open('https://www.google.com/maps/place/'+lookup)
            sys.exit()
        if event[0] == "Change addresses":
            openGoogle.close()
            meetInMiddle.close()
            break
    continue
    
    
