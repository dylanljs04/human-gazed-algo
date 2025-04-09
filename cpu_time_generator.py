#Written by David Harris-Birtill
#written on 15/04/2020
#
#Automatically create some of the computatin time lite template for reporting time
#note that this automates most of the variables, some information still needs to be edited
#these editing points are left as [] in the text.
#
#See the generated output in "Computation_time_text.txt"
#
#Run this by running the command: 
#python Computation_time_reporter.py
#
#Thanks to Abdou Rockikz for the get_size function below and suggestions for where to get system info from.

import psutil
import platform
from datetime import datetime
import sys
from datetime import date

#get_size function below by Abdou Rockikz from: https://www.thepythoncode.com/article/get-hardware-system-information-python
#date accessed 15/04/2020
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

uname = platform.uname()
cpufreq = psutil.cpu_freq()
svmem = psutil.virtual_memory()

today = date.today()
todaysDate = today.strftime("%d %B %Y")

def TimeLiteOutput():
 
  #Lite:
  #This program was tested on [insert most important hardware specifications, such as CPU name and clock frequency, number of physical cores, and GPU used], with the Operating System [insert OS, such as Windows 10 Pro or Ubuntu 18.04.3 LTS]. With this hardware and software combination the [execution time (time CPU has taken to execute program only) or response time (time taken from start to end of process, including all background processes)] for this program took [insert time with units] to complete.

  print("Computation time:")
  print("This program was tested on the "+ todaysDate+" on a computer with a " + uname.processor + "processor with a maximum clock frequency of "+str(cpufreq.max)+" MHz with "+str(psutil.cpu_count(logical=False))+" physical cores, " + str(psutil.cpu_count(logical=True))+" logical cores and " + get_size(svmem.total) + " of RAM, using the Operating System " +uname.system+ " "+uname.version+ ". With this hardware and software combination the response time (time taken from start to end of process) for this program took [insert time with units] to complete.");
  
  print()
  print("This text was generated using the open source code and text template in:")
  print('D Harris-Birtill and R Harris-Birtill, "Understanding computation time: A critical discussion of time as a computational performance metric", Time in Variance (The Study of Time XVII), Brill.');
  print()
  
  
TimeLiteOutput()

#MAKE IT SAVE THE TEXT TO A TEXT FILE
orig_stdout = sys.stdout
file_out = open('Computation_time_text.txt', 'w')
sys.stdout = file_out

TimeLiteOutput()

sys.stdout = orig_stdout
file_out.close()