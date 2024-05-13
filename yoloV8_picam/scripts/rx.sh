#!/bin/bash

#test script
echo Hello Rx
#stop management of interfac
sudo killall ifplugd
sudo ifconfig wlan1 down
sudo iw dev wlan1 set monitor otherbss fcsfail
sudo ifconfig wlan1 up
# switch channel to 13 then to 1. Quirk of channel switching
sudo iwconfig wlan1 channel 13
sudo iwconfig wlan1 channel 1
iwconfig
echo ensure freq 2.412 mode: Monitor
#activate python enviroment
cd ~/Desktop/code_test/
source ./venv/bin/activate

#run python script
sudo ~/wifibroadcast/rx wlan1 -b 1 | python yoloV8_picam/main_rx.py 
