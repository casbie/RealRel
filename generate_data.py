# -*- encoding: utf-8 -*-

#################################################
# * This file is used for generating the data   #
#	for the LDA algorithm						#
# * Author: Yu-Ju Chen                          #
# * Date: 2014-10-21                            #
#################################################

#DATA_PATH='result/2014_important/data_format.csv'
#OUTPUT_PATH='result/2014_important/training_data.csv'

import argparse

DATA_PATH='new_data_format'
OUTPUT_PATH='training_data.csv'

data={}
verb_list=[]

def read_data(path):
	fp=open(path+'/'+DATA_PATH,'r')
	count=0
	for line in fp:
		count = count + 1
		if count % 1000 == 0:
			print count
		tuples=line.strip().split(',')
		verb=tuples[0]
		pair=(tuples[1],tuples[2])
		if verb not in verb_list:
			verb_list.append(verb)
			data[verb]=[pair]
		else:
			data[verb].append(pair)

def refine_again():
    delete_list=[]
    for d in data:
        if len(data[d])<5:
            delete_list.append(d)
    print 'before refine: ' + str(len(data))
    for d in delete_list:
        del data[d]
    print 'after refine: ' + str(len(data))


def write_data(path):
	print 'start writing'
	fp=open(path+'/'+OUTPUT_PATH,'w')
	fp.write(str(len(data))+'\n')
	for v in data:
		#fp.write(v+': ')
		for i in range(0,len(data[v])):
			if i == len(data[v])-1:
				fp.write('('+data[v][i][0]+','+data[v][i][1]+')\n')
			else:
				fp.write('('+data[v][i][0]+','+data[v][i][1]+') ')


def main():
    parser = argparse.ArgumentParser(description='Generate data for LDA')
    parser.add_argument('path', type=str, help='path of data')
    args = parser.parse_args()
    path = args.path
    read_data(path)
    refine_again()
    write_data(path)


if __name__ == '__main__':
    main()
