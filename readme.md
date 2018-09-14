# TensorDetect

A code set based off tensorflow to detect objects and return their object type and coordinates over lan.

## Features

- Uses tensorflow to detect objects based on a frozen infrence graph
- Uses openCV to get the image off webcams 
- sends data over lan in packets which can be decoded as a json string


## TODO:
- Implement object selection
- Add more networking (send and recieveables via JSON)
- Camera switching (If needed, not sure)
- Auto trainer based on opencv (It is a very big hassle to run through all of the images on labelimg and to then train it)
- Verify that we can have LED strip control to make it easier to track a retro-reflective goal and not changing the parameters on the camera
- 
