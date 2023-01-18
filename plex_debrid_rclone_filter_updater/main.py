import plexapi
from plexapi.myplex import MyPlexAccount
import sched, time
import threading, random
from dotenv import load_dotenv
import os

load_dotenv()







##
## Settings and Settings Check
## 21-286


def loadsettings():
#settings from .env
    global nickname
    nickname = os.getenv("NICKNAME")
    global token
    token = os.getenv("TOKEN")
    global baseurl
    baseurl = os.getenv("BASEURL")
    global source
    source = os.getenv("SOURCE")
    global user
    user = os.getenv("USER")
    global password
    password = os.getenv("PASSWORD")
    global server
    server = os.getenv("SERVER")
    global intervall
    intervall = os.getenv("INTERVALL")
    global destination
    destination = os.getenv("DESTINATION")
    global dircachetime
    dircachetime = os.getenv("DIRCACHETIME")
    global dircachetimesetting
    dircachetimesetting = os.getenv("DIRCACHETIMESETTING")
    global vfscachemode
    vfscachemode = os.getenv("VFSCACHEMODE")
    global vfscachemodesetting
    vfscachemodesetting = os.getenv("VFSCACHEMODESETTING")
    global buffersize
    buffersize = os.getenv("BUFFERSIZE")
    global buffersizesetting
    buffersizesetting = os.getenv("BUFFERSIZESETTING")
    #setupforclient
    global tokenHost
    tokenHost = os.getenv("TOKENHOST")
    global baseurlhost
    baseurlhost = os.getenv("BASEURLHOST")
    global userhost
    userhost = os.getenv("USERHOST")
    global passwordhost
    passwordhost = os.getenv("PASSWORDHOST")
    global serverhost
    serverhost = os.getenv("SERVERHOST")
    global showwatched
    showwatched = os.getenv("SHOWWATCHED")
    global usersettingslist, rdclonesettingslist, hostsettingslist, filtersettingslist
    usersettingslist = [nickname, token, baseurl, user, password, server]
    rdclonesettingslist = [source, destination, dircachetime, dircachetimesetting, vfscachemode, vfscachemodesetting, buffersize, buffersizesetting]
    hostsettingslist = [tokenHost, baseurlhost, userhost, passwordhost, serverhost]
    filtersettingslist = [showwatched, intervall]
###
loadsettings()
###

def firstsetup():
    #create user settings
    def usersettings():
    
        global nickname, token, baseurl, user, password, server, usersettingslist
        A = input("Please provide a nickname for the client: ")
        nickname = f"{A}"
        print("Do you want to use token login or user login? Token is recommended only for local account.")
        print("Token login for external clients results in error. Known Error")
        question = input("Please write token or user : ")
        if question == "token":
            print("It is recommended to use different tokens for different instances. (eg. not the same for plex_debrid and filter_updater) ")
            print("You can visit http://plex.tv/devices.xml to find a token ")
            A = input("Please provide the token. : ")
            token = f"{A}"
            A = input("Please provide the baseurl. The standard is http://localhost:32400 : ")
            baseurl = f"{A}"
            user = False
            password = False
            server = False
            usersettingslist = ["NICKNAME="+'"'+nickname+'"',"TOKEN="+'"'+token+'"' , "BASEURL="+'"'+baseurl+'"', "USER="+'"'+str(user)+'"', "PASSWORD="+'"'+str(password)+'"', "SERVER="+'"'+str(server)+'"']
        elif question == "user":
            A = input("Please provide the username. eg. user@usermail.com : ")
            user = f"{A}"     
            A = input("Please provide the password. eg. safepass147852369 : ")
            password = f"{A}"    
            A = input("Please provide the servername. eg. PlexCloudServer : ")
            server = f"{A}"    
            token = False
            baseurl = False
            usersettingslist = ["NICKNAME="+'"'+nickname+'"',"TOKEN="+'"'+str(token)+'"' , "BASEURL="+'"'+str(baseurl)+'"', "USER="+'"'+user+'"', "PASSWORD="+'"'+password+'"', "SERVER="+'"'+server+'"']
        else:
            usersettings()


    #create rdclone settings

    def rdclonesettings():
        global source, destination, dircachetime, dircachetimesetting, vfscachemode, vfscachemodesetting, buffersize, buffersizesetting, rdclonesettingslist
        if source == "" or source == () or source == None:
            ("Next we need to setup the rclone startup settings: ") 
            A = input("Please provide the remote name as setup in rclone. eg. your-remote: : ")
            source = f"{A}"
            print("When mounting as a fixed disk dprintrive you can either mount to an unused drive letter, or to a path representing a nonexistent subdirectory of an existing parent directory or drive.")
            A = input("Please provide the destination. eg. H: or "+r"C:\User-Cloud\Nickname : ")
            destination = f"{A}"
            print("Now lets check the starting command for rclone ")
            print("The standard is --dir-cache-time 10s --vfs-cache-mode full --buffer-size 2G ")
            question = input("Do you want to use standard settings? Please answer with a simple yes or no: ")
        if question == "yes":
            dircachetime = "--dir-cache-time"
            dircachetimesetting = "10s"
            vfscachemode = "--vfs-cache-mode"
            vfscachemodesetting = "full"
            buffersize = "--buffer-size"
            buffersizesetting = "2G"
            rdclonesettingslist = ["SOURCE="+'"'+source+'"',"DESTINATION="+'"'+destination+'"' , "DIRCACHETIME="+'"'+dircachetime+'"', "DIRCACHETIMESETTING="+'"'+dircachetimesetting+'"', "VFSCACHEMODE="+'"'+vfscachemode+'"', "VFSCACHEMODESETTING="+'"'+vfscachemodesetting+'"', "BUFFERSIZE="+'"'+buffersize+'"', "BUFFERSIZESETTING="+'"'+buffersizesetting+'"']
            
        elif question == "no":
            A = input("Please provide the dir cache time command. Standard is --dir-cache-time . Leave blank if you dont want to use it. : ")
            dircachetime = f"{A}"     
            A = input("Please provide the dir cache time setting. Standard is 10s . Leave blank if you dont want to use it. : ")
            dircachetimesetting = f"{A}"    
            A = input("Please provide the vfscache command. Standard is --vfs-cache-mode . Leave blank if you dont want to use it. : ")
            vfscachemode = f"{A}"    
            A = input("Please provide the dir buffersizesetting setting. Standard is full . Leave blank if you dont want to use it. : ")
            vfscachemodesetting = f"{A}"    
            A = input("Please provide the buffersize command. Standard is --buffer-size . Leave blank if you dont want to use it. : ")
            buffersize = f"{A}"     
            print("[if you want to add different rclone startup commands just add them in the following field like you would in the commandline. Eg.: 2G --extracommand detail")
            A = input("Please provide the dir buffersizesetting. Setting standard is 2G . Leave blank if you dont want to use it. : ")
            buffersizesetting = f"{A}"    
            rdclonesettingslist = ["SOURCE="+'"'+source+'"',"DESTINATION="+'"'+destination+'"' , "DIRCACHETIME="+'"'+dircachetime+'"', "DIRCACHETIMESETTING="+'"'+dircachetimesetting+'"', "VFSCACHEMODE="+'"'+vfscachemode+'"', "VFSCACHEMODESETTING="+'"'+vfscachemodesetting+'"', "BUFFERSIZE="+'"'+buffersize+'"', "BUFFERSIZESETTING="+'"'+buffersizesetting+'"']
        else:
            rdclonesettings()
    # create host settings
    def hostsettings():
        global tokenHost, baseurl, userhost, passwordhost, serverhost, tokenhost, baseurlhost, hostsettingslist
        print("Next we need to setup the host settings. This is the account which hosts your server. This is needed to send the refresh library command")
        question = input("Is the client account also the host account? Please answer with a simple yes or no: ")
        if question == "yes":       
            userhost = user
            passwordhost = password
            serverhost = server
            tokenHost = token
            baseurlhost = baseurl
            hostsettingslist = ["TOKENHOST="+'"'+str(tokenHost)+'"',"BASEURLHOST="+'"'+str(baseurlhost)+'"' , "USERHOST="+'"'+str(userhost)+'"', "PASSWORDHOST="+'"'+str(passwordhost)+'"', "SERVERHOST="+'"'+str(serverhost)+'"']
            
        elif question == "no":
            question = input("Do you want to use token login or user login? Token is recommended. Please write token or user : ")
            if question == "token":
                print("It is recommended to use different tokens for different instances. (eg. not the same for plex_debrid and filter_updater ")
                print("You can visit http://plex.tv/devices.xml to find a token ")
                A = input("Please provide the token. : ")
                tokenHost = f"{A}"
                A = input("Please provide the baseurl. The standard is http://localhost:32400 : ")
                baseurlhost = f"{A}"
                userhost = False
                passwordhost = False
                serverhost = False
                hostsettingslist = ["TOKENHOST="+'"'+tokenHost+'"',"BASEURLHOST="+'"'+baseurlhost+'"' , "USERHOST="+'"'+str(userhost)+'"', "PASSWORDHOST="+'"'+str(passwordhost)+'"', "SERVERHOST="+'"'+str(serverhost)+'"']
            elif question == "user":
                A = input("Please provide the username. eg. user@usermail.com : ")
                userhost = f"{A}"     
                A = input("Please provide the password. eg. safepass147852369 : ")
                passwordhost = f"{A}"    
                A = input("Please provide the servername. eg. PlexCloudServer : ")
                serverhost = f"{A}"    
                tokenHost = False
                baseurlhost = False
                hostsettingslist = ["TOKENHOST="+'"'+str(tokenHost)+'"',"BASEURLHOST="+'"'+str(baseurlhost)+'"' , "USERHOST="+'"'+userhost+'"', "PASSWORDHOST="+'"'+passwordhost+'"', "SERVERHOST="+'"'+serverhost+'"']
            else:
                hostsettings()
    #create filter settings
    def filtersettings():
        global showwatched, intervall, filtersettingslist
        print("Next we need to setup the filter settings. ")
        print("Do you want to exclude shows and movies which are marked watched by the client?")
        print("To exclude watched shows and movies choose yes. To include shows and movies with watched state choose no")
        question = input("Please answer with a simple yes or no: ")
        if question == "yes":       
            showwatched = True
            filtersettingslist = ["SHOWWATCHED="+'"'+str(showwatched)+'"']

        elif question == "no":
            showwatched = False
            filtersettingslist = ["SHOWWATCHED="+'"'+str(showwatched)+'"']
        else:
            filtersettings()

        print("What is the frequency you want your watchlist to get checked? Recommended is 30 seconds.")
        question = input("Please provide a number for the intervall in seconds: ")
        
        intervall = question
        filtersettingslist = ["SHOWWATCHED="+'"'+str(showwatched)+'"', "INTERVALL="+intervall]





    def settingscheckdetail():
        global usersettingslist, rdclonesettingslist, hostsettingslist, filtersettingslist
        if None in usersettingslist or "" in usersettingslist or () in usersettingslist:
            usersettings()
        else:
            pass
        if None in rdclonesettingslist or "" in rdclonesettingslist or () in rdclonesettingslist:
            rdclonesettings()
        else:
            pass
        if None in hostsettingslist or "" in hostsettingslist or () in hostsettingslist:
            hostsettings()
        else:
            pass 
        if None in filtersettingslist or "" in filtersettingslist or () in filtersettingslist:
            filtersettings()
        else:
            pass
    settingscheckdetail()




    usersettingslist = ["NICKNAME="+'"'+nickname+'"',"TOKEN="+'"'+str(token)+'"' , "BASEURL="+'"'+str(baseurl)+'"', "USER="+'"'+str(user)+'"', "PASSWORD="+'"'+str(password)+'"', "SERVER="+'"'+str(server)+'"']
    rdclonesettingslist = ["SOURCE="+'"'+source+'"',"DESTINATION="+'"'+destination+'"' , "DIRCACHETIME="+'"'+dircachetime+'"', "DIRCACHETIMESETTING="+'"'+dircachetimesetting+'"', "VFSCACHEMODE="+'"'+vfscachemode+'"', "VFSCACHEMODESETTING="+'"'+vfscachemodesetting+'"', "BUFFERSIZE="+'"'+buffersize+'"', "BUFFERSIZESETTING="+'"'+buffersizesetting+'"']
    hostsettingslist = ["TOKENHOST="+'"'+str(tokenHost)+'"',"BASEURLHOST="+'"'+str(baseurlhost)+'"' , "USERHOST="+'"'+str(userhost)+'"', "PASSWORDHOST="+'"'+str(passwordhost)+'"', "SERVERHOST="+'"'+str(serverhost)+'"']
    filtersettingslist = ["SHOWWATCHED="+'"'+str(showwatched)+'"', "INTERVALL="+intervall]
    settings = []
    settings.append("#login settings")
    for A in usersettingslist:
        settings.append(str(A))
    settings.append("#rdclone settings")
    for A in rdclonesettingslist:
        settings.append(str(A))
    settings.append("#host settings")
    for A in hostsettingslist:
        settings.append(str(A))
    settings.append("#filter settings")
    for A in filtersettingslist:
        settings.append(str(A))

    #write os env
    with open(".env", 'w') as f:
        f.write('\n'.join(settings))
    f.close





    loadsettings()
    settingscheck()


#check if settings are loaded correctly
def settingscheck():
    settings = [nickname, token, baseurl, user, password, server, intervall, source, destination, dircachetime, dircachetimesetting, vfscachemode, vfscachemodesetting, buffersize, buffersizesetting, tokenHost, baseurlhost, userhost, passwordhost, serverhost, showwatched]
    for A in settings:
        if A == "" or A == () or A == None:
            firstsetup()
        else:
            pass
    if os.path.exists("rclone.exe") == False:
        print("Please copy the rclone.exe into the same folder as the filter_updater. Recommended is the fork RClone_RD by itsToggle")
        input("As soon as you are ready you can confirm with enter. : ")
        settingscheck()
    else:
        global nicknamesetting
        nicknamesetting = (nickname+"-filter.txt")

settingscheck()



##
## filterupdater and checker
##291-503



if token == False or token == "False":

    account = MyPlexAccount(f'{user}', f'{password}')
    plex = account.resource(f'{server}').connect()
else:
    account = MyPlexAccount(token)
    from plexapi.server import PlexServer
    plex = PlexServer(baseurl, token)

all_sections = {
    "show_sections":[],
    "movie_sections":[]
}

get_sections = plex.library.sections()
for index, section in enumerate(get_sections):
    if section.type.lower() == "show":
        all_sections['show_sections'].append(section.title)
    if section.type.lower() == "movie":
        all_sections['movie_sections'].append(section.title)


#makes all shows and movies filterable
import re
def filterfy(s):
    #remove numbers
    s = ''.join([i for i in s if not i.isdigit()])
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", ' ', s)
    # Replace all runs of whitespace with a single star
    s = re.sub(r"\s+", '*', s)
    return s

#get current time
def updatetimestamp():
    global timestamp
    import datetime
    timestamp = ('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ')

outputlist = []
oldoutputlist = []
watchlist = []


def startrclone():
    global result
    import subprocess
    command = (["rclone", "mount", source, destination, dircachetime, dircachetimesetting, vfscachemode, vfscachemodesetting, buffersize, buffersizesetting, "--ignore-case", "--filter-from", nicknamesetting])   
    result = subprocess.Popen(command) 
startrclone()

def terminaterclone():
    global result
    result.terminate()

# pushes every hour the time to inform the user that the tool is still working
def printit():
    threading.Timer(3600, printit).start()
    updatetimestamp()
    random_list = [timestamp+"I am still here, working as a donkey", timestamp+"Are you still checking in?", timestamp+"short update from me", timestamp+"When my son told me to stop impersonating a flamingo, I had to put my foot down.",timestamp+"random bullshit", timestamp+"just that you know the current time",timestamp+"thanks for checking in on me",timestamp+"Bee Boo Bipp",timestamp+"how are you?"]
    for x in range(150):
        random_list.append(timestamp+"still updating every "+os.getenv("INTERVALL")+" seconds")
    print(random.choice (random_list))



def printnewitemofoutputlist():
    # Create sets of a,b
    global outputlist
    global oldoutputlist
    #clean timestamp
    if oldoutputlist == []:
        pass
    else:
        del oldoutputlist[0]
        del outputlist[0]

    #check for differences in list elements
    setA = set(oldoutputlist)
    setB = set(outputlist)
    onlyInA = setA.difference(outputlist)
    onlyInB = setB.difference(oldoutputlist)

    if oldoutputlist == []:
        pass
    elif onlyInB != set():
        print("New item(s) added to watchlist: ", *onlyInB, sep="\n")
    if oldoutputlist == []:
        pass
    elif onlyInA != set():
        print("Item(s) deleted from watchlist: ", *onlyInA, sep="\n")
    if oldoutputlist == []:
        pass
    else:
        oldoutputlist.insert(0,"blank")
        outputlist.insert(0,"blank")

def updatefilterlist():
    global watchlist
    global outputlist

    #get current time
    updatetimestamp()
    
    #load only released shows
    watchlist = account.watchlist(filter='released')
    #adding results
    outputlist.append("#"+timestamp)
    outputlist.append("#show")
    for item in watchlist:
         if item.type == "show":
            A = (f"{item.title}")
            outputlist.append("+ *"+filterfy(A)+"*")
    outputlist.append("#movie")
    for item in watchlist:
         if item.type == "movie":
            A = (f"{item.title}")
            outputlist.append("+ *"+filterfy(A)+"*")
    outputlist.append("#filter out the rest")
    outputlist.append("- *")
    #write filter.txt 
    with open(nicknamesetting, 'w') as f:
        f.write('\n'.join(outputlist))
    f.close
    #print interface
#    print(*outputlist, sep="\n")
    printnewitemofoutputlist()
    print(timestamp,"job finished, silently refreshing every",os.getenv("INTERVALL"),"seconds")


    
def updatefilterlistonlyunwatched():
    global watchlist
    global outputlist

    #get current time
    updatetimestamp()
    watchlist = account.watchlist(filter='released')    

    #load only unwatched on watchlist results
    #adding results
    unwatchedlist = []
    for item in watchlist:
        if item.type == "show":
            if (item.viewedLeafCount) < (item.leafCount):
                A = (f"{item.title}")
                unwatchedlist.append("+ *"+filterfy(A)+"*")

    for item in watchlist:
        if item.type == "movie":
            if (item.viewCount) < 1:
                A = (f"{item.title}")
                unwatchedlist.append("+ *"+filterfy(A)+"*")                



    #load watchlist results
    #adding results
    onwatchlistlist = []
    for item in watchlist:
         if item.type == "show":
            A = (f"{item.title}")
            onwatchlistlist.append("+ *"+filterfy(A)+"*")

    for item in watchlist:
         if item.type == "movie":
            A = (f"{item.title}")
            onwatchlistlist.append("+ *"+filterfy(A)+"*")


    outputlist.append("#"+timestamp)
    outputlist.append("#show and movie mixed")
    outputlist.extend(list(set(unwatchedlist).intersection(onwatchlistlist)))
    outputlist.append("#filter out the rest")
    outputlist.append("- *")
    

    #write filter.txt 
    with open(nicknamesetting, 'w') as f:
            f.write('\n'.join(outputlist))
    f.close

    #print interface if in trouble
    #print(*outputlist, sep="\n")
    printnewitemofoutputlist()
    updatetimestamp()
    print(timestamp,"job finished, silently refreshing every",intervall,"seconds")
    
def safeoldoutputlist():
    global outputlist
    global oldoutputlist

    oldoutputlist = outputlist

def cleanoutputlist():
    global outputlist
    outputlist = []

def updateplexlibrary():
    if tokenHost == False or tokenHost == "False":
            account = MyPlexAccount(f'{userhost}', f'{passwordhost}')
            plex = account.resource(f'{serverhost}').connect()
    else:
            account = MyPlexAccount(tokenHost)
            from plexapi.server import PlexServer
            plex = PlexServer(baseurlhost, tokenHost)
    time.sleep(5)
    plex.library.update()


def checkforchanges():
    global watchlist
    

    if watchlist == account.watchlist(filter='released'):
#        print(timestamp, "no changes")
        pass
    else:
        updatetimestamp()
        print(timestamp+" Changes in watchlist detected, updating", nicknamesetting, "and restarting rclone")
        safeoldoutputlist()
        cleanoutputlist()
        if showwatched == False or showwatched == "False":

            updatefilterlist()
        else:
            updatefilterlistonlyunwatched()
        terminaterclone()
        startrclone()
        updateplexlibrary()




while True:
#    
    checkforchanges()    
    
    time.sleep(int(intervall))

