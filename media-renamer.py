# This program organizes movie and tv-show files and renames them according to the Plex preferred media library naming conventions.

# Example of video file and accompanying subtitle file
# The Departed (2006).mp4
# The Departed (2006).eng.srt

# import modules re, Path and time
import re
from pathlib import PurePath, Path
import time

# record time program starts
start_T = time.time()
localtime = time.asctime(time.localtime(start_T))

# create regular expression to match expected movie name format
movie_regex = r"(?P<title>(\w+[ .-]*)+)(?P<year>\(?(?:19|20)\d{2}\)?)"
tv_regex = r"(?P<show>(\w+[ .-]*)+)(?P<season>[sS]\d{2}[eE]\d{2})"
season_regex = r"(?:season|s)\s?(?P<season>\d{1,2})"
# compile movie_regex, tv_regex, and season_regex
movie_RE = re.compile(movie_regex)
tv_RE = re.compile(tv_regex)
season_RE = re.compile(season_regex, re.I)

# expected extensions stored in tuples
subs = '.ass', '.srt', '.sub'
video = '.m4v', '.avi', '.mkv', '.mp4'

# set p to the location/path where files to be modified are located
p = Path(<your path here>)

# START OF FUNCTION DEFINITIONS***************************

# if only 1 file is being modified do this...
def renameSingle(path_obj):
    # check match for movie regex
    mov_match = movie_RE.match(path_obj.name)
    print(mov_match)
    # if there is a movie match format final string from match groups
    if mov_match:
        title = mov_match.group('title')
        year = mov_match.group('year')
        if year:
            if '(' and ')' not in year:
                year = f"({year})"
            finalStr = title + year
        else:
            finalStr = title
    # if not a movie match assume it's a tv show and format
    elif not mov_match:
        tv_match = tv_RE.match(path_obj.name)
        print(tv_match)
        show = tv_match.group('show')
        season = tv_match.group('season')
        finalStr = show + season
    # remove unwanted symbols from name
    finalStr = finalStr.replace('.', ' ')
    # rename file and return new name for moveout function to use
    path_obj.rename(path_obj.parent.joinpath(finalStr + path_obj.suffix))
    return path_obj.parent.joinpath(finalStr + path_obj.suffix)

# if multiple files in dir need modification do this...
def renameMulti(path_obj, season):
    # if the files are part of a season of a show
    if season:
        # loop through dir and check if the items are files and if so format name and rename file with new name
        for i in path_obj.iterdir():
            if i.is_file():
                tv_match = tv_RE.match(i.name)
                print(tv_match)
                fileTitle = tv_match.group('show')
                fileSeason = tv_match.group('season')
                finalStr = fileTitle + fileSeason
                finalStr = finalStr.replace('.', ' ')
                # print(finalStr)
                i.rename(i.parent.joinpath(finalStr + i.suffix))
        # rename show's parent directory "Season xx" once all contents are renamed
        path_obj.rename(path_obj.parent.joinpath("Season " + season.group('season')))
    # if the parent directory doesn't include the season identifying features assume files are movie and subs
    elif not season:
        # format movie name based on match returned
        mov_match = movie_RE.match(path_obj.name)
        title = mov_match.group('title')
        year = mov_match.group('year')
        print(mov_match)
        if year:
            if '(' and ')' not in year:
                year = f"({year})"
            finalStr = title + year
        elif not year:
            finalStr = title
        finalStr = finalStr.replace('.', ' ')
        # print(finalStr)
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
        # rename movie parent directory finalStr without any extension
        path_obj.rename(path_obj.parent.joinpath(finalStr))

# any files passed to moveout() are moved one level up
def moveout(path_obj):
    new_path = path_obj.parents[1].joinpath(path_obj.name)
    path_obj.rename(new_path)

#calls moveout() and rename() as needed
def start():
    # print number of files initially
    print(len([x for x in p.iterdir()]),"files being processed on", localtime)
    # start iterating though main directory where all directories and files reside
    for item in p.iterdir():
        if item.suffix == ".py":
            print(item)
            continue
        elif item.is_dir():
            # store count of files/folders in directory
            file_num = len([x for x in item.iterdir()])
            # check if the folder looks like a season
            seas_match = season_RE.search(item.name)
            # if only 1 file move it out immediately
            if file_num == 1:
                for i in item.iterdir():
                    if i.is_file():
                        # rename then moveout then remove parent directory
                        moveout(renameSingle(i))
                        item.rmdir()
            # if there is more than 1 file then call renameMulti passing whether it's a season
            elif file_num > 1:
                renameMulti(item, seas_match)
        # if the item is a file go straight to renaming
        elif item.is_file():
            renameSingle(item)

# start script here
start()

# calculate time program took to execute and print to console
end_T = time.time()
elapsed_time = round((end_T - start_T), 4)
print(f"Time elapsed: {elapsed_time}s")
input('Press ENTER to exit')