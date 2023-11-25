1. create a conda environment with the environment.yml
2. make sure you are running all the scripts for the below sensors in the created environment!
3. use the scripts in conjunction with LabStreamLayer LabRecorder program(https://github.com/labstreaminglayer/App-LabRecorder/releases).

Faros:
1. connect faros to your pc using the usb cable DO NOT FIX THE USB
2. open the DATA folder 
3. run the eMotionFarosManager
4. set faros into online mode (just click the Online mode tab) and note down the mac adress
5. press save and close the (you can also sync the clock in this step by checking the Synchronize checkbox)
6. close out all the folders and disconnect the sensor
7. run the lsl extension by running faros_streamer/streamer --configure --mac <mac> --ecg_fs 1000 --acc-fs 100 --ecg-n 2
8. this should now configure the faros device now you run faros_streamer/streamer --stream --mac <mac>
9. the channels should show up in LabRecorder


Zephyr:
1. Insert Zephyr module into the bioharness
2. Hold the middle of the Zephyr device (the rubber empty circle)
3. Run App-Zephyr-main/main.py --stream
4. The channels should show up in LabRecorder


Empatica:
prerequisite: make sure you are using BLED 112 dongle.
1. Run windows server for empatica which is included in the empatica folder.
2. The server will require you to use your empatica api key. You can get the api key from the e4 manager software.
3. Turn on your Empatica E4.
4. If Empatica E4 is in list in the server gui, you are fine.
5. Now run the empatica-e4-LSL.py script.
6. The script will either connect on the first try or you will have to edit deviceID with the one shown in the script (the one shown in the windows server is usually incorrect). The script will output: "Devices available: <your device id>". If your device doesn't show up check windows server.
7. Now you should be able to see the streams show up in your LabRecorder