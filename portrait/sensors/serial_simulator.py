import serial
import random
import random
import time

# Replace '/dev/ttys00X' with the first device name from socat
ser = serial.Serial('/dev/ttys020', 9600)

i = 0
try:
    while True:
        numbers = [str(random.randint(1, 100)) for _ in range(5)]
        output = ','.join(numbers) + '\n\r'
        i+=1
        
        # dist_out= f"Dist0:{random.randint(0,127)},Dist1:{random.randint(0,127)},Dist2:{random.randint(0,127)},Dist3:{random.randint(0,127)},Dist4:{random.randint(0,127)},Dist5:{random.randint(0,127)}\r\n"
        dist_out= f"Dist0:0,Dist1:0,Dist2:0,Dist3:0,Dist4:0,Dist5:0\r\n"
        ser.write(dist_out.encode('Ascii'))
        print(f"Sent: {dist_out.strip()}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping simulation...")
finally:
    ser.close()
    print("Serial port closed.")
