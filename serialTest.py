import serial
import time

#change Serial name here
ser = serial.Serial('/dev/cu.usbmodem14201',9600)  # open serial port

# print(ser.name)         # check which port was really used
# ser = serial.Serial()
# ser.baudrate = 9600
# ser.port = '/dev/cu.usbmodem14201'
# ser.open()

print (ser)
print (ser.is_open)
time.sleep(2)

print ("11111")
ser.write(b'11111\n') 
time.sleep(1)

print ("01111")
ser.write(b'01111\n') 
time.sleep(1)

print ("00111")
ser.write(b'00111\n') 
time.sleep(1)

print ("00011")
ser.write(b'00011\n') 
time.sleep(1)

print ("00001")
ser.write(b'00001\n') 
time.sleep(1)

print ("00000")
ser.write(b'00000\n') 
time.sleep(1)

ser.close()
