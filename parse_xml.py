# -*- encoding: utf-8 -*-

#########################################################
# * This file is used for parsing xml data to json data #
#   Input: balanced data from CKIP		                #
#	Output: sentences and pos tag with json format		#
# * Thanks Mr. Aahin for encoding problem				#
# * Author: Yu-Ju Chen									#
# * Date: 2014-10-31									#
#########################################################

import codecs
import json
import io
import sys
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

reload(sys)
sys.setdefaultencoding('utf-8')

all_topic_list=[]


def transfer_xml_data(data_path):
	# tell codecs the encoding of file
	#with codecs.open(fpath, encoding='big5') as f:
	with codecs.open(data_path, encoding='big5', errors='ignore') as f:
		content = f.read()
		# now content is utf-8 encoded

	# replace encoding declaration
	content = content.replace('encoding="Big5"', 'encoding="utf-8"', 1)

	with codecs.open('tmp.xml', 'wb', encoding='utf-8') as f:
		f.write(content)

def extract_topic_data(topic_list=[]):
	data=[]
	tree = ET.parse('tmp.xml')
	root = tree.getroot()
	articles = root.iter(tag='article')
	for article in articles:
		topic = ''
		for content in article:
			if content.tag == 'topic':
				topic = content.text
				if topic not in all_topic_list:
					all_topic_list.append(topic)
			elif content.tag == 'text' and topic in topic_list:
				for sentence in content:
					#print sentence.text
					data.append(sentence.text)
	return data

def extract_all_data():
	data=[]
	tree = ET.parse('tmp.xml')
	root = tree.getroot()
	
	sentences = root.iter(tag='sentence')
	for sentence in sentences:
		data.append(sentence.text)
	
	topics = root.iter(tag='topic')
	for topic in topics:
		if topic.text not in all_topic_list:
			all_topic_list.append(topic.text)
	
	return data

def delete_same(noun_list):
    seen=[]
    for n in noun_list:
        if n not in seen:
            seen.append(n)
    return seen


def parse_data(data):
	print 'number of sentences: ' + str(len(data))
	output_data = []
	for d in data:
		#print d
		postag = d.split('　'.decode('utf8'))
		sentence = ''
		pos_list = []
		for word in postag:
			word_split = word.split('(')
			if len(word_split) != 2:
				continue
			content = word_split[0]
			tag = word_split[1][0:-1]
			sentence = sentence + content
			#print content, tag
			pos_list.append((content,tag))
		#print sentence
		output_data.append({'text':sentence, 'postag':pos_list})
	return output_data


def print_all_topic():
	for topic in all_topic_list:
		print topic


def write_data(output_file_name,output_data,index):
	fp_out=io.open(output_file_name, 'wb')
	json.dump({('2014-11-03_' + str(index)):output_data},fp_out,ensure_ascii=False)


def main():
	#fpath='Data/xmlcorpus_001.xml'
	DATA_PATH = 'Data'
	files = [ f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH,f)) ]
	#files = ['xmlcorpus_002.xml']

	final_data=[]
	for f in files:
		print f
		transfer_xml_data(DATA_PATH + '/' + f)
		data = extract_all_data()
		#extract_topic_data(['訊息'])
		output_data = parse_data(data)
		final_data = final_data + output_data

	data_num = len(final_data)
	data_num_per_file = data_num/10
	for i in range(0,10):
		start_index = data_num_per_file * i
		if i == 9:
			end_index = data_num - 1
		else:
			end_index = start_index + data_num_per_file
		write_data('output' + str(i) + '.json',final_data[start_index:end_index], i)
	print_all_topic()

if __name__ == '__main__':
	main()
