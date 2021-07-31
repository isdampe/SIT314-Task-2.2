import serial
import time
import threading
import urllib.request
import json

# Since the sensor if reading at 10HZ, this should take one second to fill up.
BUFFER_MAX_SIZE = 10

class SerialBridge:

    def __init__(self, port, baudrate = 9600):
        self.buffer = []

        while True:
            try:
                self.ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,\
                    parity=serial.PARITY_NONE,\
                    stopbits=serial.STOPBITS_ONE,\
                    bytesize=serial.EIGHTBITS,\
                    timeout=0)
                print("Done setting up serial")

                break
            except e:
                print(e)
                continue

    def loop(self):
        while True:
            line = self.ser.readline().decode().strip()
            if line:
                self.buffer.append({
                    "distanceCm": float(line), 
                    "epochMs": round(time.time() * 1000)
                })

            if len(self.buffer) > BUFFER_MAX_SIZE:
                self.consumeBuffer()

    def consumeBuffer(self):
        # Create a temporary copy of the buffer
        tmpBuffer = self.buffer.copy()

        # Empty the buffer
        self.buffer = []

        # Execute the API call in a separate thread so we're not missing sensor data
        # whilst the data is persisted...
        tmpThread = threading.Thread(target=self.postBuffer, args=(tmpBuffer,), daemon=True)
        tmpThread.start()

    def postBuffer(self, buffer):
        try:
            req = urllib.request.Request("http://localhost:4000/publish")
            req.add_header("Content-Type", "application/json; charset=utf-8")
            jsonBuffer = json.dumps(buffer).encode("utf-8")
            req.add_header("Content-Length", len(jsonBuffer))
            response = urllib.request.urlopen(req, jsonBuffer)
        except:
            pass




if __name__ == "__main__":
    sb = SerialBridge("/dev/cu.usbserial-110", 9600)
    sb.loop()