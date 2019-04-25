#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 12:27:52 2019

@author: zixuan_leah
"""

import operator
import pandas as pd


# define a function to save a list of positive and negative word
def get_pos_neg_words():
    def get_words(url):
        import requests
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

    p_url = 'http://ptrckprry.com/course/ssd/data/positive-words.txt'
    n_url = 'http://ptrckprry.com/course/ssd/data/negative-words.txt'
    positive_words = get_words(p_url)
    negative_words = get_words(n_url)
    return positive_words, negative_words


# define a function to return a list of the percentage of positive word
# and negative word for each song
def sentiment(songnames: list, lyrics: dict) -> dict:
    positive_words, negative_words = get_pos_neg_words()
    results = list()
    for song in songnames:
        cpos = cneg = 0
        for word in lyrics[song]:
            if word in positive_words:
                cpos += 1
            if word in negative_words:
                cneg += 1
        results.append((song, cpos/len(lyrics.get(song))
                        - cneg/len(lyrics.get(song))))
        result = {song[0]: song[1] for song in results}
    return result


def love(songnames: list, lovelist: list, lyrics: dict) -> dict:
    lo_dic = {}
    for name in songnames:
        match_love = 0
        lovetext = lyrics[name]
        for word in lovetext:
            if word in lovelist:
                match_love += 1
        love_rate = match_love / len(lovetext)
        lo_dic[name] = love_rate
    return lo_dic


def kid_safe(songnames, dirtylist: list, sent_rsl, lyrics: dict) -> dict:
    k_dic = {}
    for name in songnames:
        match_dirty = 0
        dirtytext = lyrics[name]
        for word in dirtytext:
            if (word in dirtylist) or ("*" in word):
                match_dirty += 1
        dirty_rate = match_dirty / len(dirtytext)
        sent_rate = sent_rsl[name]
        kidsafe_rate = 0.7 * (1 - dirty_rate) + 0.3 * sent_rate
        k_dic[name] = kidsafe_rate
    return k_dic


def length(songnames: list, lyrics: dict) -> dict:
    len_dic = {}
    for name in songnames:
        length = len(lyrics[name])
        len_dic[name] = length
    return len_dic


def complexity(songnames: list, lyrics: dict) -> dict:
    com_dic = {}
    for name in songnames:
        com = len(set(lyrics[name]))
        com_dic[name] = com
    return com_dic


def read_txt(filename: str) -> list:
    with open(filename, "r") as file:
        wl_1 = file.readlines()
        wl = []
        for words in wl_1:
            wl.append(words.strip("\n"))
    return wl


# =============================================================================
# ranking
# =============================================================================


# separate the result into two list with sorted rank
def result_rank(sentiment, love, kid_safe, length, complexity):
    result_rank_sen = sentiment
    result_rank_love = love
    result_rank_kid = kid_safe
    result_rank_len = length
    result_rank_comp = complexity
    sorted_rank_sen = dict(sorted(result_rank_sen.items(),
                                  key=operator.itemgetter(1), reverse=True))
    sorted_rank_love = dict(sorted(result_rank_love.items(),
                                   key=operator.itemgetter(1), reverse=True))
    sorted_rank_kid = dict(sorted(result_rank_kid.items(),
                                  key=operator.itemgetter(1), reverse=True))
    sorted_rank_len = dict(sorted(result_rank_len.items(),
                                  key=operator.itemgetter(1), reverse=True))
    sorted_rank_comp = dict(sorted(result_rank_comp.items(),
                                   key=operator.itemgetter(1), reverse=True))
    results = pd.DataFrame.from_dict([sorted_rank_sen, sorted_rank_love,
                                      sorted_rank_kid, sorted_rank_len,
                                      sorted_rank_comp]).T
    results.columns = ['mood', 'love', 'kid_safe', 'length', 'complexity']
    results['mood'] = pd.qcut(results['mood'], 11,
                              labels=False, duplicates='drop')
    results['love'] = pd.qcut(results['love'], 11,
                              labels=False, duplicates='drop')
    results['kid_safe'] = pd.qcut(results['kid_safe'], 11, labels=False,
                                  precision=100, duplicates='drop')
    results['length'] = pd.qcut(results['length'], 11,
                                labels=False, duplicates='drop')
    results['complexity'] = pd.qcut(results['complexity'], 11,
                                    labels=False, duplicates='drop')
    return results.applymap(lambda x: x/10)


def create_song_details_dic(song_details):
    import pandas as pd
    song_info = pd.DataFrame.from_dict(song_details).T
    song_info.columns = ['id', 'artist', 'title', 'ENG']
    song_info.drop('ENG', axis=1, inplace=True)
    return song_info
