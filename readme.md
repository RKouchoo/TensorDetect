# TensorDetect

A code set based off tensorflow to detect objects and return their object type and coordinates over lan.

## Features

- Uses tensorflow to detect objects based on a frozen infrence graph
- Uses openCV to get the image off webcams 
- sends data over lan in packets which can be decoded as a json string


## TDOD:
- implement object selection
- add more networking (send and recieveables via JSON)
- camera switching (If needed, not sure)
- auto trainer based on opencv (It is a very big hassle to run through all of the images on labelimg and to then train it)
