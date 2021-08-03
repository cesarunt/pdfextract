from werkzeug.utils import secure_filename
import psutil
from utils.config import cfg

global limitUsePercentCPU
limitUsePercentCPU = cfg.PROCESS.LIMIT_CPU

# CPU PROCESS FUNCTIONS
def get_viewProcess_CPU():
    process = True
    # Validate if server is processing by process limit
    percentAverage, percentTotal = get_useProcess_CPU()

    if (percentAverage>limitUsePercentCPU or percentTotal>limitUsePercentCPU):
        process = False
    
    return process

def get_useProcess_CPU():
    # CPU usage
    sum_cpu = 0
    percentAverage = 0
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        # print(f"Core {i}: {percentage}%")
        sum_cpu += percentage
    # print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    percentAverage = round(sum_cpu / psutil.cpu_count(), 2)
    percentTotal = round(psutil.cpu_percent(), 2)
    print('\nCalculate Percentage: ( Average %s , Total %s )'%(percentAverage, percentTotal))
   
    return percentAverage, percentTotal


# FILES FUNCTIONS
def allowed_file(file_name, file_extensions):
    if not "." in file_name :
        return False
    ext = file_name.rsplit(".", 1)[1]

    if ext.upper() in file_extensions:
        return True
    else:
        return False

def allowed_file_filesize(file_size, file_maxlength):
    if int(file_size) <= file_maxlength :
        return True
    else:
        return False