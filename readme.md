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
- Write auto trainer based on opencv (It is a very big hassle to run through all of the images on labelimg and to then train it)
- Verify that we can have LED strip control to make it easier to track a retro-reflective goal and not changing camera parameters

### Notes:

- Python JSON serialisation to dictionary accessible to java:
	`https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json/10252138#10252138`
	`data = json.dumps(myobject.__dict__)`

- Object coordinates addins:
	`https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/issues/69`
