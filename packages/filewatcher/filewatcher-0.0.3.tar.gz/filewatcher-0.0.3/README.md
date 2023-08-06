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
files_info_dict = filewatcher.get_files_info(directory='/home/krishna/mygit-repos/',recursively=True)

# Doesn't retrieve files information from sub-directories if recursively=False
files_info_dict = filewatcher.get_files_info(directory='/home/krishna/mygit-repos/',recursively=False)

# Check out an entire usage example at 
[Cyberinfy-filewatcher filewatcher_usage.py](https://github.com/cyberinfy/Tools/blob/master/filewatcher/filewatcher_usage.py)
