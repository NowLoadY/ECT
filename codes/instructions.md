# elecshooterPC.py
runs on PC, send command to the micro-controller, "AC|0|0|0" and "AA|0|0" are for aim. "ST" is for shoot. If you didn't use servo-gimbal, you should only need to send "ST" to RasPi Pico. 
details of Initialization, you can check [here](https://github.com/NowLoadY/ECT/blob/main/codes/elecshooterPC.py#:~:text=%23%20%2D%2D%2D%2Dstart%20initialize%2D%2D%2D%2D%20%23)  
yolov7 pre-trained model could be download [here](https://github.com/WongKinYiu/yolov7#:~:text=yolov7.pt%20yolov7x.pt%20yolov7%2Dw6.pt%20yolov7%2De6.pt%20yolov7%2Dd6.pt%20yolov7%2De6e.pt)  
The default target is the bottle, but you can change it [here](https://github.com/NowLoadY/ECT/blob/main/codes/elecshooterPC.py#:~:text=%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23-,%23%20%2D%2D%2D%2Danalyse%2D%2D%2D%2D%20%23,-%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23), the classes are accroding to the coco dataset.
# elecshooterPico.py  
runs on Pico. handle commands recieved from serial, and charge, shoot or aim.  
details of GPIO, you can check [here](https://github.com/NowLoadY/ECT/blob/main/codes/elecshooterPico.py#:~:text=%E5%BC%80%E5%A7%8B%E6%9E%84%E5%BB%BA%2D%2D%2D%2D%20%23-,Num_chargePin%20%3D%2018,-Num_shootPin%20%3D%2019.)  
