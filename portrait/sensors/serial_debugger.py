import serial
import time

# Replace '/dev/ttys00Y' with the second device name from socat
ser = serial.Serial('/dev/ttys021', 9600, timeout=1)

def read_serial():
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"Received: {line}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping serial reader...")
    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    print("Starting serial reader. Press Ctrl+C to stop.")
    read_serial()
