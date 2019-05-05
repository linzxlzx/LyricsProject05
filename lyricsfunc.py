#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 12:27:52 2019

@author: zixuan_leah
"""
import requests
import numpy as np
from collections import Counter, OrderedDict


# define a function to save a list of positive and negative word
def get_words(url: str) -> list:
        words = requests.get(url).content.decode('latin-1')
        word_list = words.split('\n')
        index = 0
        while index < len(word_list):
            word = word_list[index]
            if ';' in word or not word:
                word_list.pop(index)
            else:
                index += 1
        return word_list


# get neg and pos words online
def get_pos_neg_words():
    p_url = 'http://ptrckprry.com/course/ssd/data/positive-words.txt'
    n_url = 'http://ptrckprry.com/course/ssd/data/negative-words.txt'
    positive_words = get_words(p_url)
    negative_words = get_words(n_url)
    pos_w = {wd for wd in positive_words}
    neg_w = {wd for wd in negative_words}
    return pos_w, neg_w


# return percentage of positive word - negative word for each song
def mood(songnames: list, lyrics: dict) -> dict:
    positive_words, negative_words = get_pos_neg_words()
    results = {}
    for song in songnames:
        cpos = cneg = 0
        moodtext = lyrics[song]
        match_dic = Counter(moodtext)
        for word in positive_words:
            cpos += match_dic.get(word, 0)
        for word in negative_words:
            cneg += match_dic.get(word, 0)
        # we define mood result as (positive - negative)/songlength
        results[song] = ((cpos - cneg)/len(moodtext))

    return results


# return percentage of matched love related words
def love(songnames: list, lovelist: list, lyrics: dict) -> dict:
    lo_dic = {}
    for name in songnames:
        match_love = 0
        lovetext = lyrics[name]
        match_dic = Counter(lovetext)
        for word in lovelist:
            match_love += match_dic.get(word, 0)
        love_rate = match_love / len(lovetext)
        lo_dic[name] = love_rate
    return lo_dic


# return percentage of kidsafe score
def kid_safe(songnames, dirtylist: list, mood_rsl, lyrics: dict) -> dict:
    k_dic = {}
    for name in songnames:
        match_dirty = 0
        kidsafetext = lyrics[name]
        match_dic = Counter(kidsafetext)
        for word in dirtylist:
            match_dirty += match_dic.get(word, 0)
        for key in match_dic.keys():
            if "*" in key:  # include words like "f**k"
                match_dirty += match_dic[key]
        dirty_rate = match_dirty / len(kidsafetext)
        mood_rate = mood_rsl[name]
        # we also consider lyrics with stong negative moods as not kidsafe
        kidsafe_rate = 0.8 * (1 - dirty_rate) + 0.2 * mood_rate
        k_dic[name] = kidsafe_rate
    return k_dic


# return percentage of length score
def length(songnames: list, lyrics: dict) -> dict:
    len_dic = {}
    for name in songnames:
        length = len(lyrics[name])
        len_dic[name] = length
    return len_dic


# use formula for information entropy to define complexity
def complexity(songnames: list, lyrics: dict) -> dict:
    com_dic = {}
    for name in songnames:
        lyric = lyrics[name]
        counter = Counter(lyric)
        pi = np.array([x/len(lyric) for x in counter.values()])
        log2pi = np.array([np.log2(1/x) for x in pi])
        com_dic[name] = np.sum(pi*log2pi)
    return com_dic


# read wordlist for love and kidsafe dimension
# the path is relative, need to run from the root of the repo
def read_txt(filename: str) -> list:
    with open(filename, "r") as file:
        wl_1 = file.readlines()
        wl = []
        for words in wl_1:
            wl.append(words.strip("\n"))
        wordlist = {wd for wd in wl}
    return wordlist


# normalize raw scores to scale from 0.0 to 1.0 (default setting)
def result_rank(mood, love, ksafe, length, compl, details, size=11) -> dict:
    dmood = OrderedDict(sorted(mood.items(), key=lambda x: x[1]))
    dlove = OrderedDict(sorted(love.items(), key=lambda x: x[1]))
    dkid = OrderedDict(sorted(ksafe.items(), key=lambda x: x[1]))
    dlen = OrderedDict(sorted(length.items(), key=lambda x: x[1]))
    dcom = OrderedDict(sorted(compl.items(), key=lambda x: x[1]))
    dicsen = {}
    diclove = {}
    dickid = {}
    diclen = {}
    diccom = {}
    right = 0
    for i in range(0, size):
        left = right
        right += len(dmood) // size
        if i == size - 1:
            right == len(dmood)
        for j in range(left, right):
            dicsen[list(dmood)[j]] = round(i * 0.1, 1)
            diclove[list(dlove)[j]] = round(i * 0.1, 1)
            dickid[list(dkid)[j]] = round(i * 0.1, 1)
            diclen[list(dlen)[j]] = round(i * 0.1, 1)
            diccom[list(dcom)[j]] = round(i * 0.1, 1)
    # return 0.5 for foreign songs' love, mood & kidsafe dimension
    for k in range(len(dmood)):
        if details[list(dcom)[k]][3] is False:
            dicsen[list(dcom)[k]] = 0.5
            diclove[list(dcom)[k]] = 0.5
            dickid[list(dcom)[k]] = 0.5
    return dicsen, diclove, dickid, diclen, diccom


# return the list fit for json output
def get_finaldic(mood, love, kid, length, comp, detail, songname) -> list:
    rsl = []
    for name in songname:
        output = {'id': int(detail[name][0]),
                  'artist': detail[name][1],
                  'title': detail[name][2],
                  'kid_safe': kid[name],
                  'love': love[name],
                  'mood': mood[name],
                  'length': length[name],
                  'complexity': comp[name]}
        rsl.append(output)
    return rsl
