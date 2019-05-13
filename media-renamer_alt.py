# This program organizes movie and tv-show files and renames them according to the Plex preferred media library naming conventions.

# Example of video file and accompanying subtitle file
# The Departed (2006).mp4
# The Departed (2006).eng.srt

#import modules re, Path and time
import re
from pathlib import Path
import time

# record time program starts
start_T = time.time()

#create regular expression to match expected movie name format
movie_regex = r"(?P<title>(\w+[-. ]*)+)(?P<year>\(?(?:19|20)\d{2}\)?)"
tv_regex = r"(?P<show>(\w+[- .]*)+)(?P<season>[sS]\d{2}[eE]\d{2})"
season_regex = r"(?:season|s)\s?(?P<season>\d{1,2})"
#compile movie_regex, tv_regex, and season_regex
movie_RE = re.compile(movie_regex)
tv_RE = re.compile(tv_regex)
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

# if only 1 file is being modified do this...
def renameSingle(path_obj):
    mov_match = movie_RE.match(path_obj.name)
    print('movie match: ')
    print(mov_match)
    if mov_match:
        year = mov_match.group('year')
        title = mov_match.group('title')
        if year:
            if '(' and ')' not in year:
                year = f"({year})"
            finalStr = title + year
        else:
            finalStr = title
    elif not mov_match:
        tv_match = tv_RE.match(path_obj.name)
        print('tv match: ')
        print(tv_match)
        show = tv_match.group('show')
        season = tv_match.group('season')
        finalStr = show + season
    #remove unwanted symbols from name
    finalStr = finalStr.replace('.', ' ')
    path_obj.rename(path_obj.parent.joinpath(finalStr + path_obj.suffix))
    return path_obj.parent.joinpath(finalStr + path_obj.suffix)

# if multiple files in dir need modification do this...
def renameMulti(path_obj, season):
    if season:
        print(season)
        for i in path_obj.iterdir():
            if i.is_file():
                tv_match = tv_RE.match(i.name)
                print(tv_match)
                fileTitle = tv_match.group('show')
                fileSeason = tv_match.group('season')
                finalStr = fileTitle + fileSeason
                finalStr = finalStr.replace('.', ' ')
                print(finalStr)
                i.rename(i.parent.joinpath(finalStr + i.suffix))
        path_obj.rename(path_obj.parent.joinpath("Season " + season.group('season')))
    elif not season:
        print('not season')
        mov_match = movie_RE.match(path_obj.name)
        year = mov_match.group('year')
        title = mov_match.group('title')
        if year:
            if '(' and ')' not in year:
                year = f"({year})"
            finalStr = title + year
        elif not year:
            finalStr = title
        finalStr = finalStr.replace('.', ' ')
        print(finalStr)
        for i in path_obj.iterdir():
            # move subtitles out of subdirectories
            if i.is_dir():
                #move files w/subtitle file extensions to the parent directory
                for sub_file in i.iterdir():
                    if sub_file.suffix in subs:
                        moveout(sub_file)
                # remove subtitle dir once all files are moved out
                i.rmdir()
            # renaming movies
            elif i.suffix in video:
                i.rename(i.parent.joinpath(finalStr + i.suffix))
            # renaming subtitle files
            elif i.suffix in subs:
                i.rename(i.parent.joinpath(finalStr + ".eng" + i.suffix))
        path_obj.rename(path_obj.parent.joinpath(finalStr))


#moves files to parent directory and removes the old directory
def moveout(path_obj):
    print(path_obj)
    new_path = path_obj.parents[1].joinpath(path_obj.name)
    path_obj.rename(new_path)
    return path_obj

#calls moveout() and rename() as needed
def start():
    #go through all files and directories and call moveout()
    print("Number of files:", len([x for x in p.iterdir()]))
    for item in p.iterdir():
        #execute this if items in subdir
        if item.is_dir():
            #check if the folder looks like a season of show
            seas_match = season_RE.search(item.name)
            #store count of files/folders in directory
            file_num = len([x for x in item.iterdir()])
            #if only 1 file move it out immediately
            if file_num == 1:
                print('1 file only')
                for i in item.iterdir():
                    sub_seas_match = season_RE.search(item.name)
                    if i.is_dir() and sub_seas_match:
                        renameMulti(i, sub_seas_match)
                    if i.is_file():
                        # rename then moveout then remove parent directory
                        moveout(renameSingle(i))
                        item.rmdir()
            #if there is more than 1 file then call renameMulti with info whether it's a season dir or not
            elif file_num > 1:
                print('more than 1 file')
                renameMulti(item, seas_match)
        #if the item is a file go straight to renaming
        elif item.is_file():
            renameSingle(item)

#start script here
start()

#calculate time program took to execute and print to console
end_T = time.time()
elapsed_time = round((end_T - start_T), 4)
print(f"Time elapsed: {elapsed_time}s")