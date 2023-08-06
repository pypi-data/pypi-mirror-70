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
files_info_dict = filewatcher.getinfo(directory='/home/krishna/mygit-repos/',filemask='*.png',recursively=True,sortbytime=True,showprint=True)


# Doesn't retrieve files information from sub-directories if recursively=False
files_info_dict = filewatcher.getinfo(directory='/home/krishna/mygit-repos/',filemask='*',recursively=False,sortbytime=False,showprint=False)


# Check out an entire usage example with explaination at 
[Cyberinfy-filewatcher filewatcher_usage.py](https://github.com/cyberinfy/Tools/blob/master/filewatcher/filewatcher_usage.py)
