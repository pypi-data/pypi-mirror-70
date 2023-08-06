# filewatcher

This is a helper package to monitor files. You can use
[Cyberinfy-filewatcher](https://github.com/cyberinfy/Tools/blob/master/filewatcher/filewatcher_usage.py)
to write your content.

Usage:

''' 
#Install package using the below command

pip install filewatcher

'''


import filewatcher


# Retrieves files information from sub-directories too if recuresively=True
file_info_dict = get_files_info(directory='/home/krishna/mygit-repos/',filemask='*',recursively=True,sortbytime=False)

# Doesn't retrieve files information from sub-directories if recursively=False
file_info_dict = get_files_info(directory='/home/krishna/mygit-repos/',filemask='*',recursively=False,sortbytime=True)

# Check out an entire usage example at 
[Cyberinfy-filewatcher filewatcher_usage.py](https://github.com/cyberinfy/Tools/blob/master/filewatcher/filewatcher_usage.py)
