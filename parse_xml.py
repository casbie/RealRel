# -*- encoding: utf-8 -*-

#########################################################
# * This file is used for parsing xml data to json data #
#   Input: balanced data from CKIP                      #
#    Output: sentences and pos tag with json format     #
# * Thanks Mr. Aahin for encoding problem               #
# * Author: Yu-Ju Chen                                  #
# * Date: 2014-10-31                                    #
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

all_topic_list = []

all_category = ['人事', '心理', '訊息', '兒童文學', '財政', '災禍', '內政', '經濟', '民族文化', '政治現象', '影藝', '犯罪', '環保', '食物', '社會現象', '宗教', '其他文學創作', '美術', '戲劇', '資訊', '教育', '語文', '軍事', '歷史', '工程', '體育', '行銷', '交通運輸', '國家政策', '福利', '人物', '物理', '醫學', '商管', '俠義文學', '音樂', '休閒', '消費', '生物', '家庭', '建築', '傳播', '衛生保健', '公益', '天文', '農漁牧業', '司法', '政治學', '技藝', '批評與鑑賞', '統計調查', '舞蹈', '思想', '地理', '言情文學', '雕塑', '國際關係', '攝影', '文物', '藝術總論', '政黨', '電影', '衣飾', '鄉土文學', '文學通論', '考古', '社會學', '大氣科學', '數學', '礦冶', '化學', 'None']
#all_category = ['人事', '心理']


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
    data={}
    for t in topic_list:
        data[t] = []
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
                    data[topic.encode('utf-8')].append(sentence.text)
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
    #print 'number of sentences: ' + str(len(data))
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
    json.dump({('2014-11-05_' + str(index)):output_data},fp_out,ensure_ascii=False)


def main():
    #fpath='Data/xmlcorpus_001.xml'
    DATA_PATH = 'Data'
    files = [ f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH,f)) ]
    #files = ['xmlcorpus_002.xml']

    final_data = []
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


def data_stat(data):
    count_all = 0
    for topic in data:
        num = len(data[topic])
        print topic,num
        count_all = count_all + num
    print count_all


def main2():
    DATA_PATH = 'Data'
    files = [ f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH,f)) ]

    final_data = {}
    for topic in all_category:
        final_data[topic] = []

    for f in files:
        print f
        transfer_xml_data(DATA_PATH + '/' + f)
        data = extract_topic_data(all_category)
        data_count_per_file = []
        for topic in all_category:
            output_data = parse_data(data[topic])
            final_data[topic] = final_data[topic] + output_data

    for topic in all_category:
        write_data(topic + '.json',final_data[topic], 0)

    #get stat info of data (final_data)
    data_stat(final_data)


if __name__ == '__main__':
    main()
    #main2()
