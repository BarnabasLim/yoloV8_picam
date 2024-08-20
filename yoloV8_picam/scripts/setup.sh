#!/bin/bash

#test script
echo Hello world lets setup

cd ~/Desktop/code_test

#Make required dir for imagtes
mkdir -p ~/Desktop/code_test/captured_vehicle
#Make scripts executable
chmod +x -R ~/Desktop/code_test/yoloV8_picam/scripts/WORKING/
#Move scripts to desktop
cp ~/Desktop/code_test/yoloV8_picam/scripts/WORKING/* ~/Desktop/.

#Create enviroment with installed packages from the system Python
python -m venv --system-site-packages venv
#Activate python enviroment
source venv/bin/activate
#Install requirements
pip install -r ./yoloV8_picam/requirements.txt 

