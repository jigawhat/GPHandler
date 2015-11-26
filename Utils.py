import numpy as np
import os
import shutil
from datetime import datetime, date

datetime_epoch = np.datetime64('1970-01-01T00:00:00Z')
datetime_second = np.timedelta64(1, 's')

# Create a folder at the given path, if overwrite, delete existing folder and create a new empty one
def create_folder(path, overwrite=False):
    if(os.path.isdir(path)):
        if(overwrite):
            shutil.rmtree(path)
        else:
            return
    os.mkdir(path)

def timestamp():
    return datetime_to_epoch(datetime.now())

def epoch_to_lontime(epoch):
    return (epoch / 31556926.0) + 1970.0

def datetime64_to_epoch(dt64):
    return (dt64 - datetime_epoch) / datetime_second

def datetime_to_epoch(dt):
    return datetime64_to_epoch(np.datetime64(dt))

def datetime64_to_lontime(dt64):
    return epoch_to_lontime(datetime64_to_epoch(dt64))

def lontime_to_datetime64(lontime):
    return epoch_to_datetime64(lontime_to_epoch(lontime))

def lontime_to_epoch(lontime):
    return (lontime - 1970.0) * 31556926.0
                                
def epoch_to_datetime64(epoch):
    return (epoch * datetime_second) + datetime_epoch

# Converts to lontime, then adds or subtracts around ~1 hour time noise to prevent training conflicts
def datetime64_to_tinynoised_lontime(dt64):
    return apply_noise(datetime64_to_lontime(dt64), 0.0001)

# Does the same but also converts back to datetime64
def datetime64_to_tinynoised_datetime64(dt64):
    return apply_noise(dt64, datetime_second * 6000)

def apply_noise(number, noise_magnitude):
    return number + (2 * noise_magnitude * (np.random.random() - 0.5))
