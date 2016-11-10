import serial

# init 
ser = serial.Serial()  
ser.baudrate = 115200  
ser.port = "COM6"
ser.timeout = 1
print(ser)

# open
ser.open()
print("Open port success!\n" if ser.isOpen() else "Open port failed!\n")

# write and read
ser.write(b"\xAA\x00\x00\x33\x00\x00\x00\x00\x33\xAA")
msg = ser.read(10)
# The 'msg' is <type 'str'> in python2 and <class 'bytes'> in python3.
# print(type(msg))
sentence = msg.lstrip(b"\xbb").rstrip(b"\xbe")
# python2
# print(sentence)
# python3
print(sentence.decode("gb2312"))

# close
#ser.close()
#print(ser.isOpen())
