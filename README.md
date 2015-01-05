RealRel
=======

### Proposed Topic
To find out the relation between 2 pairs with given corpus

### Proposed Method
1. Cluster the noun pairs by LDA as groups, assuming each group present one relation
2. Select the seed from the groups as training data
3. With the training data, learn the model to decide the relation between each pair

### Files
#### preprocessing
* parse_xml.py: Parse the Sinica corpus(xml format) file to json format
  - Usage: python parse_xml.py
  - with function 'main': Extract all sentences and save as 10 files
  - with function 'main2': Extract data and save by category
  - the function main and main2 are only allow to change within the code

* statistics.py: Count the number of verbs and noun pairs
  - Usage: python statistic.py [data path] [file name] [output dir]
  - File names: seperated by ',' for example: 01,02,03,04
  - The output files contains
    1. verb_stat: (verb, count)
    2. noun_stat: (noun, count)
    3. pair_stat: (pair, count)
    4. data_format: (verb, pair))
    - all are not sorted, please use util/sort_data for sort

* refine_data.py: find out the verb or noun pair with small number
  - Usage: python refine_data.py [data path] [output dir] [verb threshold] [noun threshold]
  - The output files is the lists of verbs and pairs, which will be kept. The files are named as 'refined_noun' and 'refined_verb'

* delete_small.py: delete the verb and noun pair from the small list
  - Usage: python delete_small_data.py [path]
  - The output file is the refined data as format of (verb, pair), saved in file 'new_data_format'

* generate.py: generate the data for LDA
  - Usage: python generate.py [path]
  - The output file format follows the tool GibbsLDA++(http://gibbslda.sourceforge.net/)

#### util
* sort_data.py: Sort the data in given file and write the sorted data as new file
  - Usage: python sort_dat.py [input file name] [outout file name] [index]
  - The input file and output file must be csv format, and the index means the column to be sorted.

#### Data
* Categories of data: 
  - all_category = ['人事', '心理', '訊息', '兒童文學', '財政', '災禍', '內政', '經濟', '民族文化', '政治現象', '影藝', '犯罪', '環保', '食物', '社會現象', '宗教', '其他文學創作', '美術', '戲劇', '資訊', '教育', '語文', '軍事', '歷史', '工程', '體育', '行銷', '交通運輸', '國家政策', '福利', '人物', '物理', '醫學', '商管', '俠義文學', '音樂', '休閒', '消費', '生物', '家庭', '建築', '傳播', '衛生保健', '公益', '天文', '農漁牧業', '司法', '政治學', '技藝', '批評與鑑賞', '統計調查', '舞蹈', '思想', '地理', '言情文學', '雕塑', '國際關係', '攝影', '文物', '藝術總論', '政黨', '電影', '衣飾', '鄉土文學', '文學通論', '考古', '社會學', '大氣科學', '數學', '礦冶', '化學']

### Author
I am a master student from National Taiwan University.

