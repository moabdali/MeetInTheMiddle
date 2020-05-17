MeetInTheMiddle is designed to let friends type in their addresses and find a central spot to meet up without having to argue over who has to drive the most.  It finds a central point (weighted average, so if a lot of people live in one city, they'll skew the average toward themselves... the needs of the many outweighs the needs of the poor person who lives far away) for everyone to meet up in, and directly opens google maps so that you can easily search for the closest restaurant or park to meet up at.


v 0.1 - no error checking, can crash if geopy doesn't respond in a timely manner

The only special note to the reader is that you must install geopy.  To do this simply do:

pip install geopy


Or go to https://geopy.readthedocs.io/en/stable/#installation for more information


v 0.2 

- Now uses a pySimple GUI for prettier input
   – error checking on number of cars; geopy can still crash though
- To do: implement a text based save system that keeps track of previous successful addresses and allows you to access them from a drop down
- Open google maps from within a window instead of opening browser perhaps

