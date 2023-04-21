import serial

serialPort = serial.Serial(port = "COM5", baudrate=9600,
                           timeout=2, stopbits=serial.STOPBITS_ONE)

serialString = ""                           # Used to hold data coming over UART


while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        serialString = serialString.decode('Ascii')
        #print(serialString)
        distances = []
        for dist in serialString.split(','):
            distances.append(float(dist.split(':')[1]))
        print(distances)

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        # serialPort.write(b"Thank you for sending data \r\n")
