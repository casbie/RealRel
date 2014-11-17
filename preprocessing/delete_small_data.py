# -*- encoding: utf-8 -*-

#################################################
# * This file is used for re-generate the data  #
#   for the LDA algorithm                       #
# * Author: Yu-Ju Chen                          #
# * Date: 2014-10-22                            #
#################################################

import csv

small_pair_list=[]
small_verb_list=[]

data=[]

def read_data(path):
    csv_pair=open(path+'/refined_pair', 'r')
    csv_verb=open(path+'/refined_verb', 'r')
    csv_data=open(path+'/data_format', 'r')

    input_reader=csv.reader(csv_pair, delimiter=',')
    print 'read pair'
    for row in input_reader:
        small_pair_list.append((row[0],row[1]))

    input_reader=csv.reader(csv_verb, delimiter=',')
    print 'read verb'
    for row in input_reader:
        small_verb_list.append((row[0]))

    input_reader=csv.reader(csv_data, delimiter=',')
    print 'read data'
    for row in input_reader:
        verb=row[0]
        pair=(row[1],row[2])
        if verb in small_verb_list and pair in small_pair_list:
            data.append(row)
        else:
            continue

def write_data(path):
    print 'write data'
    csv_output=open(path+'/new_data_format', 'w')
    output_writer=csv.writer(csv_output, delimiter=',')
    output_writer.writerows(data)


import argparse
def main():
    parser = argparse.ArgumentParser(description='remove sparse and general data')
    parser.add_argument('path', help='path of file')
    args = parser.parse_args()
    path = args.path
    read_data(path)
    write_data(path)

if __name__ == '__main__':
    main()
