#This program organizes your files and renames them according to my preferred media library naming conventions.

#TMDB api key = 8a1f98648f69ed38fc3b24187574cd73

#Example of video file and accompanying subtitle file
#The Departed (2006).mp4
#The Departed (2006).en.srt

""" 
Step by step psuedo-code:
1.Move all files to root of folder, at maximum there will be files one dir deep from script location.
2.look at file name, remove excess characters, append date to end of filename in parentheses.
3.If subtitle file exists then give it the same name as the media file except needs extra .en suffix.
4.If no subtitle files are present in a dir, move media file to the root of the main dir so the file isn't in another sub-folder.
5.Delete empty folders.
"""
#import necessary modules re and Path
import re
from pathlib import Path

#create regular expression to match expected movie name format 
movie_regex = r"(?P<title>[-0-9a-zA-Z]+[ .]*)+(?P<year>[(]?[19-20]\d{2}[)]?)"
#tv_regex = r""
#compile movie_regex
movie_RE = re.compile(movie_regex)
#tv_RE = re.compile(tv_regex)

#expected extensions stored in tuples
subs = '.ass', '.srt', '.sub'
video = '.m4v', '.avi', '.mkv', '.mp4'

#set p to the path of the current directory
p = Path('.')

#List to store all modified title strings
raw_strings = []
final_strings = []

#START OF FUNCTION DEFINITIONS*******
#renaming function using RE on path object names
def rename(path_obj, re_type):
    match = re_type.match(path_obj.name)
    tempStr = match[0]
    raw_strings.append(tempStr)
    #loop through list and fix filenames
    for item in raw_strings:
        cleaned = item.replace('.', ' ')
        final_strings.append(cleaned)
    #this will go through all file names and rename them according to the new final_strings list
    for item in p.iterdir():
        #replace name portion leaving extension untouched
        if item.is_file():
            pass
        #replace entire name with name from final_strings
        elif item.is_dir():
            item.rename()
            for sub_file in item:
                if sub_file.suffix in video:
                    #replace name with name from final_strings
                    pass
                elif sub_file.suffix in subs:
                    #add .en before suffix
                    pass

#moveout function moves files to parent directory and removes the old directory.
def moveout(path_obj):
    for item in path_obj:
        new_path = item.parent.joinpath(item)
        item.rename(new_path)
    path_obj.rmdir()

#START OF FUNCTION CALLS*****
#rename every root level file/folder
for item in p.iterdir():
    rename(item, movie_RE)

#go through all files and directories apply moveout() function when needed
for item in p.iterdir():
    if item.is_dir():
        file_counter = 0
        #count number of files/folders in directory
        for i in item.iterdir():
            file_counter += 1
            if i.is_dir():
                moveout(i)

print(raw_strings)
print(final_strings)
