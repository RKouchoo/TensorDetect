# TensorDetect

A code set based off tensorflow to detect objects and return their object type and coordinates over lan.

## Features
- Uses tensorflow to detect objects based on a frozen infrence graph
- Uses openCV to get the image off webcams 
- sends data over lan in packets which can be decoded as a json string


## REALISTIC TODO:
- Clean up detection code
- Make code modular and support detection for different objects
- Write a wholesome training tutorial/script
- Choose the best hardware platform that has a GPU (mobile quadcore i7 only pushes ~15fps whereas dual 980ti 6GB cards push 70+)
  ((Needs to be compact so it can fit on a robot without a subteam war.. *sigh*))
- Possible use of the jetson that we already have but the latest version which compiles is the 2017 binary.. also requires much work to get going. Would be easier to have newer hardware as we wont have to wait 3 hours for the binary's to compile on a new box.

## TODO:
- Implement object selection
- Add more networking (send and recieveables via JSON)
- Camera switching (If needed, not sure)
- Write auto trainer based on opencv (It is a very big hassle to run through all of the images on labelimg and to then train it)
- Verify that we can have LED strip control to make it easier to track a retro-reflective goal and not changing camera parameters

## Testing

#### ~20 FPS on a modern 6 core intel core i7 processor overclocked to 4GHz:
![alt text](https://image.ibb.co/ksNkwe/tensor_6core.png)

#### ~30fps (video framerate) on dual GTX 980ti 6GB GPU's using 5GB of vram. live framerate should be around 90fps 
![alt text](https://preview.ibb.co/kAEC9z/tensor_dualgpu.png)

### Notes:
- Python JSON serialisation to dictionary accessible to java:
	`https://stackoverflow.com/questions/10252010/serializing-class-instance-to-json/10252138#10252138`
	`data = json.dumps(myobject.__dict__)`

- Object coordinates addins:
	`https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/issues/69`
