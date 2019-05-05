#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:42:39 2019

@author: zixuan_leah
"""

import os
import nltk
nltk.download('wordnet')
nltk.download('stopwords')


def read_path(path: str) -> dict:
    names = os.listdir(path)
    buffer = {}
    for songtxt in names:
        if songtxt.endswith(".txt"):
            with open(path + "/" + songtxt, encoding="utf8") as lyrics_context:
                buffer[songtxt] = lyrics_context.readlines()
    return buffer


def read_lyrics(filedict: dict) -> (list, dict):
    names = list(filedict.keys())
    lyrics = {}
    for song in names:
            text = ''
            for sentence in filedict[song]:  # split into sentences
                text += sentence.strip("\r\n")+" "
            words = text.split(" ")  # split into words as a list
            word_list = []
            for letters in words:  # take off chars "...", ","...
                word_adj = ''.join([char.lower() for char in letters
                                    if (char.isalpha()
                                        or char == "'"  # "it's" as word
                                        or char == "*"  # "f**k" as word
                                        or char == "-")])  # "o-o-oh" as word
                if not (word_adj == '' or word_adj == "-" or word_adj == "'"):
                    if "-" in word_adj:  # split "Rang-dang-digidy-dang-a-dang"
                        sub_words = word_adj.split("-")
                        word_list.extend(sub_words)
                    else:
                        word_list.append(word_adj)

            lyrics[song] = word_list  # txtname as key, lyric wordlist as value

    return names, lyrics  # return songnames list and lyrics dictinary


# func used to detct whether is english song
def detect_lang(songwords: list) -> bool:
    from nltk.corpus import stopwords
    from nltk.corpus import wordnet
    index = 0
    count = 1
    stop = 20  # we take the first 20 words to detct whether it is english
    eng_words = 0
    words_chosen = []
    stop_words = set(stopwords.words('english'))
    if len(songwords) < stop:
        stop = len(songwords)
    while count <= stop and index <= len(songwords) - 1:
        if songwords[index].isalpha():
            if not (songwords[index] in words_chosen
                    or (songwords[index] in stop_words)):
                words_chosen.append(songwords[index])
                if wordnet.synsets(songwords[index]):
                    eng_words += 1
                count += 1
        index += 1
    if count < stop:
        stop = count
# we set the criteria: English song has 70% of first 10 words as English
# take into consideration of slangs like 'yo', 'umm'...
    if eng_words / stop >= 0.7:
        return True
    else:
        return False


# func to store song name, id, artist and English detection result
def get_details(namelist: list, lyricdic: dict) -> dict:
    song_details = {}
    for txtname in namelist:
        txt = txtname.rstrip(".txt")
        song_de = txt.split("~")
        for de_index in range(len(song_de)):
            song_de[de_index] = song_de[de_index].replace("-", " ")
            detect_res = detect_lang(lyricdic[txtname])
        song_de.append(detect_res)  # also append the language result
        song_details[txtname] = song_de
    return song_details  # key: txtname, value: [id, artist, name, T/F]
