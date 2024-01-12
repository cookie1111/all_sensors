import socket
import time
import pylsl


# SELECT DATA TO STREAM
LSL_streams = {}

serverAddress = '127.0.0.1'
serverPort = 28000
bufferSize = 4096


def prepare_LSL_streaming(tags):
    print("Starting LSL streaming")
    for tag in tags:
        print(f"creating stream {tag}")
        infoTag = pylsl.StreamInfo(tag,'Tag',1,nominal_srate=64,channel_format='int32',source_id='Task_tag');
        outletTag = pylsl.StreamOutlet(infoTag)
        LSL_streams[tag] = (infoTag,outletTag)
    return LSL_streams


def stream(button):

    print(f"Streaming {button} label")
    
    timestamp = time.time()
    LSL_streams[button][1].push_sample([1],timestamp=timestamp) 
    time.sleep(0.2)
    LSL_streams[button][1].push_sample([0],timestamp=timestamp)
