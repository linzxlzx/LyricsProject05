#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:22:41 2019

@author: zixuan_leah
"""

import lyricsfunc
import load
import json
import sys


def main(path = None):
    names_buffer = load.read_path(path)
    names_list, song_lyrics = load.read_lyrics(names_buffer)
    song_details = load.get_details(names_list, song_lyrics)
    love_l = lyricsfunc.read_txt("love_words.txt")
    notsafe_l = lyricsfunc.read_txt("not_kidsafe.txt")
    sent_dic = lyricsfunc.sentiment(names_list, song_lyrics)
    kidsafe_dic = lyricsfunc.kid_safe(names_list, notsafe_l, sent_dic,song_lyrics)
    love_dic = lyricsfunc.love(names_list, love_l,song_lyrics)
    length_dic = lyricsfunc.length(names_list,song_lyrics)
    com_dic = lyricsfunc.complexity(names_list,song_lyrics)
    sentdic, lovedic, kidsafedic, lengthdic, comdic = lyricsfunc.result_rank(sent_dic, love_dic, kidsafe_dic, length_dic, com_dic,song_details)
    result = lyricsfunc.get_finaldic(sentdic, lovedic, kidsafedic, lengthdic, comdic, song_details,names_list)
    finalresult = {}
    finalresult["characterizations"] = result
    json.dump(finalresult, sys.stdout, indent=4)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('LyricsProject')
    parser.add_argument('lyrics_path', help='Path to the Lyrcis folder')
    args = parser.parse_args()

    lyric_path = args.lyrics_path
#     lyric_path = "Lyrics"    
    main(lyric_path)