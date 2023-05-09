coonect to rpi via putty

ip addr is 192.168.22.178
user pi
passwd raspberry

get this computers ip addres - probably 192.168.23.157

libcamera-vid --inline -t 0 --codec mjpeg -o udp://192.168.23.157:1234 --width 2000 --height 2000 --framerate 8



---- LIGHTS

channel 1 - 72
channel 2 - 69