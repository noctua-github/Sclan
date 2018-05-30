import socket
import sys
import subprocess
import os
import time
import platform
from datetime import datetime as dt
import argparse
os.system('clear')
try:
	global parser
	global delay
	global interface
	global args
	parser = argparse.ArgumentParser(description='\033[01;31mLAN HOSTNAME SCANNER.\033[0m\n\n')
	parser.add_argument("-i","--interface", help="\033[01;31mINTERFACE.\033[0m\n\n")
	parser.add_argument("-d","--delay", help="\033[01;31mDELAY TIME BEFORE EACH SCAN.\033[0m\n\n",required=True)
	parser.add_argument("-p","--prefix", help="\033[01;31mNETWORK PREFIX.\033[0m\n\n",required=False)
	args=vars(parser.parse_args())
except:
    print("\n\n\033[01;31mUSAGE\033[01;37m: \033[01;37mpython \033[01;37m%s \033[01;31m[\033[01;37mINTERFACE\033[01;31m] [\033[01;37mPREFIX \033[01;31m(\033[01;37mOPTIONAL\033[01;31m)]\033[0m\n" %(sys.argv[0]) )
    print("\033[01;31mFOR MORE HELP, USE THE \033[01;37m -h \033[01;31m ARGUMENT.\n\n")
    sys.exit()
def log(msg):
    sys.stdout.write( "\033[01;32m[%s] \033[01;37m%s" %(str(dt.now())[11:19],str(msg)) )
def processlog(msg):
    sys.stdout.write( "\033[01;33m[%s] \033[01;37m%s" %(str(dt.now())[11:19],str(msg)) )
def errlog(msg):
    sys.stdout.write( "\033[01;31m[%s] \033[01;37m%s" %(str(dt.now())[11:19],str(msg)) )
global s
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    #s.connect(('google.com',80))
	a=([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
	[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
	log( "internet connection is up.\n".upper() )
except:
    errlog( "internet connection is down.\n".upper() )
    sys.exit()
time.sleep(0.2)
import subprocess
def prefixer():
	try:
		global prefix
		if args['prefix']:
			pass
		else:
			try:
				processlog("CHECKING INTERFACE: ["+args['interface']+"]...")
				time.sleep(0.2)
				print("\033[01;37m\n\n")
				print("\033[01;05;37m{}\033[0m\033[01;02;37m".format(str(args['interface'])))
				sys.stdout.write("\nLOCAL IP: %s"%(a))
				#subprocess.check_call("ifconfig %s |grep inet"%(str(args['interface'])),shell=True)
				sys.stdout.write("\033[01;37m")
				#subprocess.check_call("ifconfig %s |grep ether"%(str(args['interface'])),shell=True)
				print("\033[01;0m\n\n")
				print("")
				prefix=raw_input("\033[01;31m[\033[01;37m>\033[01;31m] \033[01;37mPREFIX\033[01;31m [\033[01;37m{}\033[01;31m]:\033[01;37m ".format(args['interface']))
			except subprocess.CalledProcessError as errmsg:
				errlog("\033[01;37mno interface named %s: %s.\n\n" %(args['interface'],errmsg) )
				sys.exit()
	except:
		errlog("UNKNOWN ERROR.\n")
		sys.exit()
def scanner():
	global suffix
	suffix=[]
	time.sleep(1)
	print("")
	for i in range(255):
		suffix.append(i)
		sys.stdout.write("\r"+"\033[01;33m[%s] \033[01;37mSUFFIX\033[01;31m => \033[01;37m%s ADDED FOR SCANNING.    "%(str(dt.now())[11:19],str(i)))
		sys.stdout.flush()
		time.sleep(0.001)
	print("")
	time.sleep(1)
	os.system('clear')
	print("\033[01;37mSCANNING\033[01;31m...\033[0m\n")
	connected=[]

	#disconnected=[]
	global start_time
	global total_hosts
	global no_hosts
	start_time=dt.now()
	total_hosts=0
	no_hosts=0
	for x in suffix:
		try:
			time.sleep(float(args['delay']))
			if args['prefix']:
				HOST=socket.gethostbyaddr(str(args['prefix'])+"."+str(x))
			else:
				HOST=socket.gethostbyaddr(str(prefix)+"."+str(x))
			if args['prefix']:
				details=("\r\033[01;37m%s.%s \033[01;31m => \033[01;03;37m%s"%(str(args['prefix']),str(x),HOST[0]))
			else:
				details=("\r\033[01;37m%s.%s \033[01;31m => \033[01;03;37m%s"%(str(prefix),str(x),HOST[0]))
			total_hosts=total_hosts+1
			if args['prefix']:
				if a == args['prefix']+"."+str(x):
					details=details+("     \033[01;05;31m[\033[01;37mYOU\033[01;31m]\033[0m")
			else:
				if a == prefix+"."+str(x):
					details=details+("     \033[01;05;31m[\033[01;37mYOU\033[01;31m]\033[0m")
			connected.append(details)
			print(details)
		except:
			details=("\033[01;37m%s.%s \033[01;31m NOT FOUND."%(args['prefix'],str(x)))
			#disconnected.append(details)
			no_hosts=no_hosts+1
			pass
	global stop_time
	stop_time=dt.now()
	global total_time
	total_time=stop_time-start_time
	time.sleep(0.5)
	sys.stdout.write("\033[0m")
	print("")
	log("\033[01;37mFINISHED.\n\n\n")
def details():
	print("\033[01;37mDETAILS\033[01;31m:\033[01;37m\n")
	log("TOTAL TIME: "+str(total_time)[2:10]+"\n")
	log("HOSTS FOUND: "+str(total_hosts)+"\n")
	log("HOSTS NOT FOUND ON SUBNET: "+str(no_hosts))
	print("\n\n\n")
	sys.exit()
def main():
	prefixer()
	scanner()
	details()
if __name__ == '__main__':
	main()
