# -*- coding: utf-8 -*- 

from twython import TwythonStreamer
from twython import Twython
import socket
import time
import threading
import serial
import json
import os
import sys
from shutil import copyfile
APP_KEY=""
APP_SECRET=""
OAUTH_TOKEN=""
OAUTH_TOKEN_SECRET=""
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
restartFlag=False


class TwitterStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
	    global streamFailed
	
            friends=read_friends()
            user=data['user']['id']
            print "user"
            print user
            if str(user) in friends:
                print "user detected"
		twitter.retweet(id=data['id'])
            else: 
                print "user is not detected"
	    streamFailed=False

    def on_error(self, status_code, data):
	global streamFailed
	streamFailed=True
        print(status_code)
	twitter.update_status(status='hata verdim kardes')

def get_friends():
	tysfriends = twitter.get_friends_ids(screen_name="gokberkoguz")
	friendsFile = open(resource_path("txt_files/friends.txt"),"w")
	for friend_id in tysfriends['ids']:
	    print friend_id
	    friendsFile.write(str(friend_id) + "\n")  
	print len(tysfriends['ids'])
	friendsFile.close()
def read_friends():
    with open(resource_path("txt_files/friends.txt"), "r+") as f:
	
        friends = [x.strip() for x in f.readlines()]
    return friends
def read_terms():
    with open(resource_path("txt_files/terms.txt"), "r+") as f:
        terms = [x.strip() for x in f.readlines()]
	terms = ','.join(str(x) for x in terms)
	print terms
    	return terms
def start_stream(terms):
	stream = TwitterStreamer(APP_KEY, APP_SECRET,
		            OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	stream.statuses.filter(track=terms)
class UDPListener():
    def __init__(self):
		self.UDP_PORT_Listen=5130
        self.isOpen = True
        self.threadClass=self.ThreadClass(self)
        self.threadClass.start()
    class ThreadClass(threading.Thread):        
            def __init__(self,udpListener):
                threading.Thread.__init__(self)
                self.udpListener = udpListener
            def run(self):
                print "Udp Listener has been started!\n"
                self.udpListener.threadFunction()
                self.isRunning = False
                print "Udp Listener  thread is not running right now"
    def threadFunction(self):
        global incomingData,dataChanged,restartFlag
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        currentIP = s.getsockname()[0]
        #currentIP=os.popen('ip addr show wlan').read().split("inet ")[1].split("/")[0] #changes according to the internet connection type 
        self.sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
        self.sock.bind((currentIP, self.UDP_PORT_Listen))
	
        print "ses1"
        while self.isOpen:
		try:
		    time.sleep(0.1)
		    self.data, self.addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
		    print self.data
		    self.data=self.data.decode('UTF-8')
		    json_string = json.loads(self.data)
		    sendCommand=(json_string['command'])
		    if sendCommand=="addterm":
			term=(json_string['name'])
			with open(resource_path("txt_files/terms.txt"), "a") as f:
				f.write("\n"+term) 
				f.close()
		    if sendCommand=="removeterm":
			term=(json_string['name'])
			with open(resource_path("txt_files/terms.txt"), "r") as f:
				terms = f.readlines()
				f.close()
				print terms
			with open(resource_path("txt_files/terms.txt"), "w") as f:
				try:
					terms.remove(term+'\n')
				except:
					print "cannot find term"
				for x in terms:
	  				f.write("%s" % x)
		    if sendCommand=="getfriends":
				get_friends()
		    if sendCommand=="restart":
			restartFlag=True
			self.sock.close()
			restart()
		except:	
			print "something went wrong"

def restart():
        import sys
		print("Waiting for restart")
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")

        import os
        os.execv(sys.executable, ['python'] + sys.argv)
					
def resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)


UDPListener()
terms=read_terms()
print("booting up")
time.sleep(15)
print("booting finished")
streamFailed=True
while(streamFailed):
	try:
		start_stream(terms)
		time.sleep(5)
	except:
		twitter.update_status(status='hata verdim kardes')
		streamFailed=True
		time.sleep(180)





