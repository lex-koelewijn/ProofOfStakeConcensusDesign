import os

# Check if the required subdirectories exist and create them when required. 
def directoryCheck():     
    if(not os.path.exists('./img')):
        os.mkdir('./img')
    
    if(not os.path.exists('./img/all')):
        os.mkdir('./img/all')