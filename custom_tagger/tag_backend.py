import socket
import time
import pylsl


# SELECT DATA TO STREAM
tags = []

serverAddress = '127.0.0.1'
serverPort = 28000
bufferSize = 4096


def prepare_LSL_streaming():
    print("Starting LSL streaming")
    if tags:
        infoTag = pylsl.StreamInfo('tag','Tag',1,channel_format='float32',source_id='Task_tag');
        global outletTag
        outletTag = pylsl.StreamOutlet(infoTag)
prepare_LSL_streaming()

time.sleep(1)


def reconnect():
    print("Reconnecting...")
    connect()
    suscribe_to_data()
    stream()

def stream():
    last_ibi_time = None  # Variable to store the time of the last IBI event
    frequency = None
    try:
        print("Streaming...")
        while True:
            try:
                response = s.recv(bufferSize).decode("utf-8")
                #print(response)
                if "connection lost to device" in response:
                    #print(response.decode("utf-8"))
                    reconnect()
                    break
                samples = response.split("\n")
                #print(samples)
                for i in range(len(samples)-1):
                    stream_type = samples[i].split()[0]
                    
                    if stream_type == "E4_Acc":
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = [int(samples[i].split()[2].replace(',','.')), int(samples[i].split()[3].replace(',','.')), int(samples[i].split()[4].replace(',','.'))]
                        outletACC.push_sample(data, timestamp=timestamp)
                    if stream_type == "E4_Bvp":
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = float(samples[i].split()[2].replace(',','.'))
                        #print(timestamp)
                        outletBVP.push_sample([data], timestamp=timestamp)
                        #print("E4_bvp")
                    if stream_type == "E4_Ibi":
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = float(samples[i].split()[2].replace(',','.'))
                        outletIBI.push_sample([data], timestamp=timestamp)
                    if stream_type == "E4_Gsr":
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = float(samples[i].split()[2].replace(',','.'))
                        outletGSR.push_sample([data], timestamp=timestamp)
                    if stream_type == "E4_Temperature":
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = float(samples[i].split()[2].replace(',','.'))
                        outletTemp.push_sample([data], timestamp=timestamp)
                    if stream_type == "E4_IbiXDXD": #delete XDXD if you want to check the ibi frequency
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = float(samples[i].split()[2].replace(',','.'))                        
                        if last_ibi_time is not None:
                            interval = timestamp - last_ibi_time  # Calculate time interval between IBIs
                            frequency = 1 / interval  # Calculate frequency in Hertz (Hz)
                            print(f"IBI Frequency: {frequency} Hz length of data: {len(data) if type(data) == list else 1 }")
                        last_ibi_time = timestamp  # Update the last IBI time
                    if stream_type == "E4_Tag":
                        timestamp = float(samples[i].split()[1].replace(',','.'))
                        data = float(samples[i].split()[2].replace(',','.'))
                        print(samples[i])
                        print(data,timestamp)
                        outletTag.push_sample([data], timestamp=timestamp)
                #time.sleep(1)
            except socket.timeout:
                print("Socket timeout")
                reconnect()
                break
    except KeyboardInterrupt:
        print("Disconnecting from device")
        s.send("device_disconnect\r\n".encode())
        s.close()
stream()
