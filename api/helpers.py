import re
from datetime import datetime
import os
import csv



def log_error(status_error):
    """
    creates directory for storing logs for the day

    return: None

    """
    today, now = datetime.today(), datetime.now()

    
    directory = 'errorlog'
    if not os.path.exists(directory):
        os.makedirs(directory)

    error_csv = str(today)+"_"+str(now.hour)+':'+str(now.minute)+':'+ str(now.second), status_error
    error_file = open(str(directory)+'/betconv'+str(directory)+'.csv', 'a+')
    with error_file:
        writer = csv.writer(error_file)
        writer.writerow(error_csv)
    return