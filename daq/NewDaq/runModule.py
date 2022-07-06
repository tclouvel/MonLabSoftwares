import time
from multiprocessing import Process
from threading import Thread
import sys
import yaml
import daqModule as daq
import daqModuleDevice0 as daq0
import daqModuleDevice1 as daq1

devFile = "Example_settings.yaml"
InitFlag = False

def load_dev(config_file):
    #Read config file and return device and daq settings
    if(config_file=="Example_settings.yaml" or config_file =='-help'):
        fileEx = open('Example_settings.yaml')
        print("Contents of example settings file (Example_settings.yaml):")
        print("##################################")
        print(" ")
        for line in fileEx:
            print(line)
        print("##################################")
        print(" ")
        return 0,0,0
    else:
        with open(config_file,"r") as f:
            config = yaml.safe_load(f)
            DeviceSettings = config[0]["DeviceSettings"]
            DaqSettings = config[1]["DaqSettings"]
            ChannelSettings = config[2]["ChannelSettings"]
        return DeviceSettings, DaqSettings, ChannelSettings

def load_sig(sig_file):
    if(sig_file=="Example_settings.yaml" or sig_file =='-help'):
        fileEx = open('Example_settings.yaml')
        print("Contents of example settings file (Example_settings.yaml):")
        print("##################################")
        print(" ")
        for line in fileEx:
            print(line)
        print("##################################")
        print(" ")
        return 0,0,0
    else:
        with open(sig_file,"r") as f:
            sig = yaml.safe_load(f)
            SigSettings = sig[0]["SigSettings"]
        return SigSettings
    

def InitDAQ(DeviceInfo,DAQSettings,ChannelSettings):
    Stat = daq.init_daq(DeviceInfo,DAQSettings,ChannelSettings) #initialise daq with specified parameters
    return Stat

def RunDAQ(SubRun,Settings,Stat):
    #Collect specified number of triggers a total of nSub times by running run_daq function 
    Modules = [daq0.run_daq,daq1.run_daq] #Add more for more devices...
    Processes = [None]*len(Settings)
    RetStats=[]
    for j in range(len(Settings)): 
        RetStats.append(Stat[2*j])
        RetStats.append(False)
    for i in range(len(Settings)):
        Processes[i] = Thread(target = Modules[i], args = (SubRun,Settings[i],Stat[2*i],RetStats,2*i))
        Processes[i].start()
    time.sleep(2)
    Check=False
    while(Check  == False):
        Check = True
        for l in range(int(len(RetStats)/2)):
            if(RetStats[l+1]==False):Check=False
    for p in Processes: p.join()
    return RetStats

def RunAmpDAQ(SubRun,Settings,Stat,SigGen):
    #Collect specified number of pulse captures
    daq0.run_amp_daq(SubRun,Settings,Stat,SigGen)    



def CloseDAQs(Settings,Stat): 
    for i in range(len(Settings)): daq.close(Settings[i],Stat[2*i]) #close the daq
    return

if __name__ == "__main__":
    print("^^^ Picoscope libraries called ^^^")
    args=sys.argv
    if(len(args)!=2): #print out help if the number of arguments are wrong
       print(" ")
       print("To use DAQ, run:")
       print(" ")
       print("python3.7 RunDAQ.py YourDAQandDeviceSettings.yaml")
       print(" ")
       print("For more details on settings:")
       print(" ")
       print("python3.7 RunDAQ.py -help")
       print(" ")
    else:   
       devFile = args[1] #read in specified settings file
       main() 

