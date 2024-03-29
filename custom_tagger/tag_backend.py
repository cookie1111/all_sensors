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
    LSL_streams = {}
    for tag in tags:
        print(f"creating stream {tag}")
        infoTag = pylsl.StreamInfo(tag,'Tag',1,nominal_srate=2,channel_format='int32',source_id='Task_tag');
        outletTag = pylsl.StreamOutlet(infoTag)
        LSL_streams[tag] = (infoTag,outletTag)
    return LSL_streams


def stream(button, value):
    if value == 1:
        print(f"Streaming {button} label")
    timestamp = time.time()
    LSL_streams[button][1].push_sample([value],timestamp=timestamp) 

def stream_all(button):
    timestamp = time.time()