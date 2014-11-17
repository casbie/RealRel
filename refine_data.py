# -*- encoding: utf-8 -*-

#################################################
# * This file is used for refine the data which #
#   is used for training the LDA		        #
#	- modify the N data (remove #<10)			#
#	- modify the V data (remove #<100)			#
# * Author: Yu-Ju Chen                          #
# * Date: 2014-10-20 created                    #
#         2014-11-14 modified                   #
#################################################

import argparse

data_file='data_format'
verb_count_file='verb_stat'
pair_count_file='pair_stat'

data_verb={}
data_verb_list=[]
data_pair={}
data_pair_list=[]
verb_count={}
small_verb_count={}
pair_count={}
small_pair_count={}


def read_data(path, MAX_VERB, MIN_VERB, MIN_PAIR):

	print 'I am reading verb_count_file.'
	fp = open(path+'/verb_stat', 'r')	
	for line in fp:
		data = line.strip().split(',')
		verb = data[0]
		count = int(data[1])
		verb_count[verb] = count
		if count > MIN_VERB and count < MAX_VERB:
			small_verb_count[verb] = count
	fp.close()

	print 'I am reading pair_count_file.'
	fp = open(path+'/pair_stat','r')
	for line in fp:
		data = line.strip().split(',')
		pair = (data[0],data[1])
		count = int(data[2])
		pair_count[pair] = count
		if count > MIN_PAIR:
			small_pair_count[pair] = count
	fp.close()

#not used
def delete_small_pair():
	for p in small_pair_count:
		count = small_pair_count[p]
		if p in pair_count:
			del pair_count[p]
		if p in data_pair:	
			for v in data_pair[p]:
				verb_count[v] = verb_count[v] - 1
				#"minus one" assumes one pair appear once in one verb
				if p in data_verb[v]:
					data_verb[v].remove(p)

#not used
def delete_small_verb():
	for v in small_verb_count:
		count = small_verb_count[v]
		if v in data_verb:
			for p in data_verb[v]:
				if p in pair_count:
					pair_count[p] = pair_count[p] - 1
		if v in verb_count:
			del verb_count[v]
		if v in data_verb:
			del data_verb[v]

#not used
def write_data():
	fp = open(DATA_PATH + '/new_' + data_file, 'w')
	for v in data_verb:
		for item in data_verb[v]:
			fp.write(v + ',' + item[0] + ',' + item[1] + '\n')
	fp.close()

	fp=open(DATA_PATH + '/new_' + pair_count_file, 'w')
	for p in pair_count:
		fp.write(p[0] + ',' + p[1] + ',' + str(pair_count[p]) + '\n')
	fp.close()

	fp=open(DATA_PATH + '/new_' + verb_count_file, 'w')
	for v in verb_count:
		fp.write(v + ',' + str(verb_count[v]) + '\n')
	fp.close()


def write_small_list(path):
	print 'I am writing.'
	fp = open(path+'/refined_pair', 'w')
	for p in small_pair_count:
		fp.write(p[0] + ',' + p[1] + ',' + str(small_pair_count[p]) + '\n')
	fp.close()

	fp = open(path+'/refined_verb','w')
	for v in small_verb_count:
		fp.write(v + ',' + str(small_verb_count[v]) + '\n')
	fp.close()


def main():
	parser = argparse.ArgumentParser(description='delete sparse and general data')
	parser.add_argument('path', type=str, help='the directory of file')
	parser.add_argument('max_verb', type=int, help='maximum number of verb')
	parser.add_argument('min_verb', type=int, help='minimum number of verb')
	parser.add_argument('min_pair', type=int, help='minimum number of pair')
	args = parser.parse_args()
	path = args.path
	max_v = args.max_verb
	min_v = args.min_verb
	min_p = args.min_pair
	read_data(path, MAX_VERB=max_v, MIN_VERB=min_v, MIN_PAIR=min_p)

	#delete_small_pair()
	#delete_small_verb()
	#write_data()
	write_small_list(path)


if __name__ == '__main__':
	main()
