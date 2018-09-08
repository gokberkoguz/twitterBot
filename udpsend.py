import socket

UDP_IP = "192.168.1.105"
UDP_PORT = 5005
#MESSAGE = "Hello, World!"
    
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

while True:
    ses=raw_input("What do you wanna command to Computer\n")
    if (ses=="addterm") or (ses=="removeterm"):
	var=raw_input("What is your variable?\n")
    MESSAGE= '''{"name": "'''+var+'''","command":"'''+ses+'''"}'''
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
