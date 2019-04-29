#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:22:41 2019

@author: zixuan_leah
"""

from lyrics_function import *
from load import *
import json
import pandas as pd

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('LyricsProject')
    parser.add_argument('lyrics_path', help='Path to the Lyrcis folder')
    args = parser.parse_args()

    lyric_path = args.lyrics_path
#    lyric_path = "Lyrics"

    names_list, song_lyrics = read_lyrics(lyric_path)
    song_details = get_details(names_list, song_lyrics)
#    
    love_l = read_txt("love_words.txt")
    notsafe_l = read_txt("not_kidsafe.txt")
    sent_dic = sentiment(names_list, song_lyrics)
    kidsafe_dic = kid_safe(names_list, notsafe_l, sent_dic,song_lyrics)
#    #print(kidsafe_dic)
    love_dic = love(names_list, love_l,song_lyrics)
    length_dic = length(names_list,song_lyrics)
#    
    com_dic = complexity(names_list,song_lyrics)
#    
    
#    import pandas as pd
    result_0 = create_song_details_dic(song_details).join(result_rank(sent_dic, love_dic, kidsafe_dic, length_dic, com_dic))
    result_1 = list()
    for song in names_list:
        result_1.append(result_0.T.to_dict()[song])
        
    finalresult={"characterizations":result_1}
#    finalresult=result_rank(sent_dic, love_dic, kidsafe_dic, length_dic, com_dic).T.to_dict()
#
    json.dump(finalresult, sys.stdout, indent = 4)