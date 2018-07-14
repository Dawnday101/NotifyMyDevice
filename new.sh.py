#! /usr/bin/env python
import sys,os,subprocess
class Bash2Py(object):
  __slots__ = ["val"]
  def __init__(self, value=''):
    self.val = value
  def setValue(self, value=None):
    self.val = value
    return value

def GetVariable(name, local=locals()):
  if name in local:
    return local[name]
  if name in globals():
    return globals()[name]
  return None

def Make(name, local=locals()):
  ret = GetVariable(name, local)
  if ret is None:
    ret = Bash2Py(0)
    globals()[name] = ret
  return ret

def Str(value):
  if isinstance(value, list):
    return " ".join(value)
  if isinstance(value, basestring):
    return value
  return str(value)

class Expand(object):
  @staticmethod
  def hash():
    return  len(sys.argv)-1

#########################################################################################
### androidNotifty.sh        	#
### Script for sending notifications using "Notify My Androids" API    #
###    Author : Markp1989@gmail.com  Version: 25JULY2011  #
#########################################################################################
## Requirements:	curl        	#
#########################################################################################
## Usage: androidNotify.sh "Application Name" "Event Name" "Some Details" [priority]	#
#########################################################################################
## API Documentation:	https://www.notifymyandroid.com/api.jsp      #
#########################################################################################
#####start user configurable settings####
APIkey=Bash2Py("eb11126e1ee9e24be2c65e9363d9300f2a620220d96792cf")
## API Key must me set here, go to http://www.notifymyandroid.com/ to get one
limit=Bash2Py(5)
# how many times to attempt to run curl, can help on unstable networks.
pinghost=Bash2Py("google.com")
##host to ping before running anything to verify that the internet is up.
#####end user configurable settings######
##renaming parameters to make rest of the code more readable.
command=Bash2Py(__file__)
application=Bash2Py(sys.argv[1])
event=Bash2Py(sys.argv[2])
description=Bash2Py(sys.argv[3])
priority=Bash2Py(sys.argv[4])
##the urls that are used to send the notification##
baseurl=Bash2Py("https://www.notifymyandroid.com/publicapi")
verifyurl=Bash2Py(str(baseurl.val)+"/verify")
posturl=Bash2Py(str(baseurl.val)+"/notify")
##choosing a unique temp file based on the time (date,month,hour,minute,nano second),to avoid concurent usage interfering with each other
notifyout=Bash2Py("/tmp/androidNotify"+os.popen("date \"+%d%m%Y%H%M%S%N\"").read().rstrip("\n"))
usage=Bash2Py("Usage: "+str(command.val)+" Application Event Description [priority]")
##exit functions so i dont have to keep writing the same exit messages for every fail. 
def error_exit () :
    global errormessage
    global usage
    global application
    global event
    global description
    global priority

    ##this function is used to exit the program in the event of an error.
    print( "%s\\n\\t%s\\n\\t\\t%s\\n" % ("[ Error ] Notification not sent:", str(errormessage.val), str(usage.val)) )
    
    print( "\\n%s\\n" % (str(application.val)+" , "+str(event.val)+" , "+str(description.val)+", priority="+str(priority.val)) )
    
    ##adding info used to tmp file. 
    exit(1)

def clean_exit () :
    global notifyout

    print( "%s\\n" % ("[ info ] Notification sent") )
    
    _rc0 = subprocess.call(["rm",str(notifyout.val)],shell=True)
    ##removing output file when notification was sent okay
    exit(0)

def pre_check () :
    global errormessage
    global pinghost

    ##this function checks that curl is installed, and that an internet connection is available 
    if not subprocess.call("which" + " " + "curl",shell=True,stdout=file('/dev/null','wb'))
    :
        
            Make("errormessage").setValue("curl is required but it's not installed, exiting.")
            error_exit()
    
    ##checking that the machine can connect to the internet by pinging the host defined in $pinghost
    if not subprocess.call("ping" + " " + "-c" + " " + "5" + " " + "-w" + " " + "10" + " " + str(pinghost.val),shell=True,stdout=file('/dev/null','wb'))
    :
        
            Make("errormessage").setValue("internet connection is required but not connected, exiting.")
            error_exit()
    

def input_check (_p1,_p2,_p3,_p4,_p5) :
    global errormessage
    global priority

    ##this section checks that the parameters are an acceptable length if any of these tests fail then the program exits.
    ##the API will send an error back if the data sent is invalid, but no point in knowingly sending incorrect information.
    #API key must be 48 characters long, just because the APIkey is the right length doesnt mean its valid,the API will complain if it is invalid.
    if (Expand.hash()APIkey != 48 ):
        Make("errormessage").setValue("APIkey must be 48 characters long, you gave me "+str(Expand.hash()APIkey))
        error_exit()
    elif (#application must be between 1 and 256 characters long
    Expand.hash()application > 256 or Expand.hash()application < 1 ):
        Make("errormessage").setValue("[ error ] the application parameter is invalid or missing")
        error_exit()
    elif (#event must be between 1 and 1000 characters long
    Expand.hash()event > 1000 or Expand.hash()event < 1 ):
        Make("errormessage").setValue("[ error ] the event parameter is invalid or missing")
        error_exit()
    elif (#description must be between 1 and 1000 characters long
    Expand.hash()description > 1000 or Expand.hash()description < 1 ):
        Make("errormessage").setValue("[ error ] the description parameter is invalid or missing")
        error_exit()
    ##priority is expected to be between -2 and 2, if other numbers are given than default(0) is used.
    if (str(priority.val) == '' ):
        print( "%s\\n" % ("priority is not set , must be between -2 and 2, using 0 instead") )
        
        Make("priority").setValue(0)
    elif (int(priority.val) > 2 or int(priority.val) < -2 ):
        print( "%s\\n" % ("priority "+str(priority.val)+" is invalid, must be between -2 and 2, using 0 instead") )
        
        Make("priority").setValue(0)
    if (str(_p5) != '' ):
        Make("errormessage").setValue("[ error ] too many parameters have been provided:")
        error_exit()

def send_notification () :
    global complete
    global tries
    global limit
    global APIkey
    global application
    global event
    global description
    global priority
    global posturl
    global notifyout

    ##sending the notification using curl
    #if curl failes to complete then it will try again, untill the "limit" is met,or curl runs ok.
    Make("complete").setValue(0)
    tries=Bash2Py(0)
    while (int(complete.val) < 1 and int(tries.val) < int(limit.val)):
        #if curl is already running that we wait up to a minute before proceding
        if (os.popen("pidof curl").read().rstrip("\n") != '' ):
            print( "%s\\n" % ("another instance of curl is running, waiting up to 1 minute before trying.") )
            
            subprocess.call(["sleep",str((RANDOM.val % 60))],shell=True)
        ##waiting up to 1 minute as running multiple instances of curl at a time was causing some to fail on my machine.
        if subprocess.call(["curl","--silent","--data-ascii","apikey="+str(APIkey.val),"--data-ascii","application="+str(application.val),"--data-ascii","event="+str(event.val),"--data-asci","description="+str(description.val),"--data-asci","priority="+str(priority.val),str(posturl.val),"-o",str(notifyout.val)],shell=True):
            Make("complete").setValue(1)
        Make("tries").setValue(str(tries.val)+"+1")

def check_notification () :
    global notifyout
    global errormessage

    ##checking that the notification was sent ok.
    ##api returns message 200 if the notification was sent
    if (subprocess.call(["grep","-q","200",str(notifyout.val)],shell=True) ):
        clean_exit()
    else:
        ##getting the error reported by the API, this may break if the API changes its output, will change as soon as I can find a commandline xml parser
        Make("errormessage").setValue(os.popen("cut -f4 -d'>' "+str(notifyout.val)+" | cut -f1 -d'<'").read().rstrip("\n"))
        error_exit()

##running the functions
pre_check()
input_check()
send_notification()
check_notification()
