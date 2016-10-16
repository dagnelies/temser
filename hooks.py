import os
import os.path

def dir(param, parsed, current_path):
    return os.path.listdir(current_path + '/' + param)