from geopy.geocoders import Nominatim   #geolocation use pip install geopy
import webbrowser                       #open google maps

#initialize geolocator
geolocator = Nominatim(user_agent="MeetInTheMiddle")





print("This program accepts the addresses of your friends (and yourself) and finds a\nfair middle ground to meet at.  This program will assume each car is \none data point.")
print("*"*75)
getInput = (input("How many cars will be driven? \n>> "))
friendNum = (int)(getInput)
print("*"*75)
friendArray = [] #array to keep track of each friend's location in lat long


for i in range (0,friendNum):
    while True:
        inputAddress = input("What is car "+(str)(i+1)+"'s current address?  Provide at least a street and city at minimum.\n>> ")
        location =(geolocator.geocode(inputAddress)) #convert input to detailed address
        print("Assuming address is: "+(str)(location.address)) #convert to street address
        print("Is this good? y for yes, otherwise n to try again.\n")
        getInput = input(">> ")
        if getInput == "y":
            print("*"*75)
            break
        else:
            continue
    friendArray.append((location.latitude, location.longitude))


latiAverage = 0.0
longAverage = 0.0


for i in range (0,friendNum):
    latiAverage = latiAverage + friendArray[i][0]
    longAverage = longAverage + friendArray[i][1]

latiAverage = latiAverage / friendNum
longAverage = longAverage / friendNum
#averages out the lat long


latLongAverage = (latiAverage,longAverage)
#combine lat and long into one entry for easier usage

#turn the latlong average into a real address (geopy attempts to use the closest address it can find)
location = geolocator.reverse(latLongAverage)


print("\nThe closest known fair address is:\n "+(str)(location.address))
print("*"*75)
print("\nThe latitude longitude is "+str(latLongAverage))
print("*"*75)
lookup = str(latLongAverage[0])+','+str(latLongAverage[1])
getInput = (input("Open Google Maps?  y/n \n>> "))

if getInput == "y":
            webbrowser.open('https://www.google.com/maps/place/'+lookup)
else:
    exit()
