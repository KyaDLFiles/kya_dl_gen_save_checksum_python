# kya_dl_gen_save_checksum_python
Port of the [original written in C](https://github.com/KyaDLFiles/kya\_dl\_gen_save\_checksum)  
Fixes the checksums inside Kya: Dark Lineage save files (and possibly other Eden Games games that use the same libraries or code?) so that the game accepts them as valid  
Also supports the [May 12 prototype](https://hiddenpalace.org/Kya:_Dark_Lineage_\(May_12,_2003_prototype\)) (the [September 29 prototype](https://hiddenpalace.org/Kya:_Dark_Lineage_\(Sep_29,_2003_prototype\)) save files work like the final game)

# Usage
Requires Python 3.4 (3.4.4 - the latest that runs on XP - tested and working)  
`gensavecsum.py /path/to/save/file.dat <--verbose> <--game_ver=\[game version\]>`  
The checksums stored in the file will be fixed  
`--verbose` makes the program print the calculated checksums and data block sizes  
`--game_ver` can be:
- `final`: for the final version of the game and September 29 prototype, default value
- `may12`: for the May 12 prototype
## Return codes
*0: ran succesfully*  
*1: error opening file*  
*2: missing argument*  
*3: file isn't a KDL save file*  
*4: bad file header, invalid section size value(s) (program has tried to read out of bounds)*  
*5: invalid argument(s)* 

# Documentation
https://kyadlfiles.github.io/technical/#save_header (refers to the final game)

GIGANTIC thanks to [avail](https://github.com/avail) (_cherry_ on Discord) for helping with this!
