# media-renamer version 0.2 (October 2020)
Utility to rename media files (movies and tv shows) in a standardized format so media scanners like Plex fetch correct metadata efficiently.

---

## How to use:
1. On **line 11** ensure the path to where the files to be modified are is enclosed inside the parentheses as well as single or double quotes.
   - If the directory your files are located in is named "media" then you can put the *media-renamer.py* file one directory above and change the line to: `p = Path("./media")`
   - Alternatively the *media-renamer.py* files can be located anywhere as long as you include the absolute path.
2. Currently subtitles nested two directories deep are moved to the same level as the media file and not renamed. *I plan on adding that functionality in a future update.*
   - Additionally subtitle renaming for tv-shows is not functioning yet.
3. When done renaming all files you will be asked to press enter. This is designed so users can observe the progress/matches. If the python window closes immediately then you know an error has occured.
4. Once the path is set properly all that needs to be done is either double click on the *media-renamer.py* file or run `python3 <path to media-renamer.py>`
---
## Example results:
### Before

Movies

*Directory:* Mad.Max.Beyond.Thunderdome.1985.720p.BluRay.H264.AAC

*Video File:* Mad.Max.Beyond.Thunderdome.1985.720p.BluRay.H264.AAC.mp4

*Subtitle File:* Mad.Max.Beyond.Thunderdome.1985.720p.BluRay.H264.AAC.srt

TV Shows

*Directory:* The Orville Season 1 Complete 720p HDTV x264

*Video File:* The Orville S01E01 Old Wounds.mkv

### After

Movies

*Directory:* mad max beyond thunderdome (1985)

*Video File:* mad max beyond thunderdome (1985).mp4

*Subtitle File:* mad max beyond thunderdome (1985).eng.mp4

TV Shows

*Directory:* the orville season 01

*Video File:* the orville s01e01.mkv
