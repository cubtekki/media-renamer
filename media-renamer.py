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

""" 
New step-by-step:
- Move files to root level if only 1 file is present in directory
- Move subtitle files from nested sub-dirs
- Rename all files in root dir using desired format
- Apply root level names to sub-dir file names according to type
"""
#import necessary modules re and Path
import re
from pathlib import Path
import time

start_T = time.time()

#create regular expression to match expected movie name format
movie_regex = r"(?P<title>(\w+[-. ]*)+)(?P<year>\(?(?:19|20)\d{2}\)?)"
# tv_regex = r"(?P<title>(\w+[- .]*)+)(?P<season>[sS]\d{2}[eE]\d{2})"
season_regex = r"season\s?\d{,2}"
#compile movie_regex, tv_regex, and season_regex
movie_RE = re.compile(movie_regex)
# tv_RE = re.compile(tv_regex)
season_RE = re.compile(season_regex, re.I)

#expected extensions stored in tuples
subs = '.ass', '.srt', '.sub'
video = '.m4v', '.avi', '.mkv', '.mp4'

#set p to the path of the directory where files are located
p = Path(r"D:\Dropbox\01_schoolThumbDrive\cs231_advPython\final_project\00_testing")

#empty lists to store all original and modified title strings
raw_strings = []
final_strings = []

#START OF FUNCTION DEFINITIONS***************************

#renaming function using RE on path object names
def rename():
    for f in p.iterdir():
        print(f.name)
        # seas_match = season_RE.search(f.name)
        # print('seasmatch complete')
        # tv_match = tv_RE.match(f.name)
        mov_match = movie_RE.match(f.name)
        # print('movmatch complete')
        if mov_match:
            year = mov_match.group('year')
            # title = mov_match.group('title')
            if year:
                if '(' and ')' not in year:
                    year = f"({year})"
                finalStr = mov_match.group('title') + year
            else:
                finalStr = mov_match.group('title')
    #remove unwanted symbols from name
        finalStr = finalStr.replace('.', ' ')
        final_strings.append(finalStr)
    counter = 0
    #loop through list of altered names and files and match them up
    for f in p.iterdir():
        if counter < len(final_strings):
            if f.is_dir():
                for item in f.iterdir():
                    if item.suffix in video:
                        item.rename(item.parent.joinpath(final_strings[counter] + item.suffix))
                    elif item.suffix in subs:
                        item.rename(item.parent.joinpath(final_strings[counter] + ".eng" + item.suffix))
                f.rename(f.parent.joinpath(final_strings[counter]))
            elif f.is_file():
                f.rename(f.parent.joinpath(final_strings[counter] + f.suffix))
            counter += 1
    print(final_strings)

#moveout function moves files to parent directory and removes the old directory.
def moveout(path_obj):
    new_path = path_obj.parents[1].joinpath(path_obj.name)
    # print(new_path)
    path_obj.rename(new_path)

#START OF FUNCTION CALLS*******************************
#start() function calls the rest
def start():
    #go through all files and directories apply moveout() function when needed
    print("Number of files:", len([x for x in p.iterdir()]))
    for item in p.iterdir():
        if item.is_dir():
            #store count of files/folders in directory
            file_num = len([x for x in item.iterdir()])
            #if only 1 file move it out immediately
            if file_num == 1:
                for i in item.iterdir():
                    if i.is_file() and i.suffix in video:
                        moveout(i)
                        #remove parent folder after moving out only file
                        i.parent.rmdir()
            #if there is more than 1 file then determine if the files are tv episodes or subtitles
            elif file_num > 1:
                for i in item.iterdir():
                    #if there's a directory that doesn't include 'season' in its name
                    if i.is_dir() and not season_RE.search(i.name):
                        #move files w/subtitle file extensions to the parent directory
                        for sub_file in i.iterdir():
                            if sub_file.suffix in subs:
                                moveout(sub_file)
                        # remove subtitle dir once all files are moved out
                        i.rmdir()
    #call rename function once files are structured properly
    rename()

start()

#calculate time program took to execute and print to console
end_T = time.time()
elapsed_time = round((end_T - start_T), 4)
print(f"Time elapsed: {elapsed_time}s")
