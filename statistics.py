# -*- encoding: utf-8 -*-

##################################################################
# * This file is used for analyze the dataset.                   #
#   1. read the pos-tagged data from file                        #
#   2. extract the noun_list and verb_list                       #
#    3. count                                                    #
#       - pair histogram                                         #
#       - verb histogram                                         #
# * Input command:                                               #
#                                                                #
#    python statistic.py [data path] [file name] [output dir]    #
#                                                                #
#    File names are seperated by ','                             #
#    For example: 01,02,03,04                                    #
#                                                                #
# * Author: Yu-Ju Chen                                           #
# * Date: 2014-10-18 created                                     #
#          2014-11-12 modified                                   #
##################################################################

import json
import io
import sys
import os


def read_input(data_path, file_name_list):
    for f in file_name_list:
        fp=open(data_path + '/' + f + '.json')
        data = json.load(fp)
        for article in data:
            print article
            new_data_sentence = data[article]
            print 'number of sentence: ' + str(len(new_data_sentence))
            count = 0
            for sentence in new_data_sentence:
                count = count + 1
                if count % 1000 == 0:
                    print count
                noun_list = []
                verb_list = []
                for word in sentence['postag']:
                    text = word[0]
                    flag = word[1]
                    
                    if flag[0:2] == 'Na' or flag[0:2] == 'Nb' or flag[0:2] == 'Nc':
                        noun_list.append(word[0])
                    elif flag[0] == 'V':
                        verb_list.append(word[0])
                    else:
                        continue
                noun_list = delete_same(noun_list)
                verb_list = delete_same(verb_list)
                noun_pair_list = stat_for_pair(noun_list)
                stat_for_verb(verb_list,noun_pair_list)


def delete_same(noun_list):
    seen = []
    for n in noun_list:
        if n not in seen:
            seen.append(n)
    return seen


global_pair_list = []
global_pair_count = {}
def stat_for_pair(noun_list):
    noun_pair_list = []
    for i in range(0, len(noun_list)-1):
        for j in range(i+1, len(noun_list)):
            pair = (noun_list[i], noun_list[j])
            noun_pair_list.append(pair)
            if pair not in global_pair_list:
                global_pair_list.append(pair)
                global_pair_count[pair] = 1
            else:
                global_pair_count[pair] = global_pair_count[pair] + 1
    return noun_pair_list


global_verb_list = []
global_verb_count = {}
global_verb_pair_list = {}


def stat_for_verb(verb_list, noun_pair_list):
    for v in verb_list:
        num_noun_pair = len(noun_pair_list)
        if v not in global_verb_list:
            global_verb_list.append(v)
            global_verb_count[v] = num_noun_pair
            global_verb_pair_list[v] = []
        else:
            global_verb_count[v] = global_verb_count[v] + num_noun_pair
        
        for pair in noun_pair_list:
            global_verb_pair_list[v].append(pair)


def write_pair_stat(output_dir):
    fp_out = io.open(output_dir + '/' + 'pair_stat', 'wb')
    for p in global_pair_count:
        fp_out.write((p[0] + ',' + p[1] + ',' + str(global_pair_count[p]) + '\n').encode('utf-8'))


def write_verb_stat(output_dir):
    fp_out = io.open(output_dir + '/' + 'verb_stat', 'wb')
    for v in global_verb_count:
        fp_out.write((v + ',' + str(global_verb_count[v]) + '\n').encode('utf-8'))


def write_data_format(output_dir):
    fp_out = io.open(output_dir + '/' + 'data_format', 'wb')
    for v in global_verb_pair_list:
        if len(global_verb_pair_list) == 0:
            continue
        for pair in global_verb_pair_list[v]:
            fp_out.write((v + ',' + pair[0] + ',' + pair[1] + '\n').encode('utf-8'))


def main():
    #data_path='../Data/udn/2014_people/pos'
    #file_name_list=['01','02','03','04']

    data_path = sys.argv[1]
    file_name = sys.argv[2]
    output_dir = sys.argv[3]
    
    file_name_list = file_name.split(',')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    read_input(data_path, file_name_list)
    write_pair_stat(output_dir)
    write_verb_stat(output_dir)
    write_data_format(output_dir)


if __name__ == '__main__':
    main()
