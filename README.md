RealRel
=======

##### Proposed Topic
To find out the relation between 2 pairs with given corpus

##### Proposed Method
1. Cluster the noun pairs by LDA as groups, assuming each group present one relation
2. Select the seed from the groups as training data
3. With the training data, learn the model to decide the relation between each pair

##### Files
#### Preprocessing
* parse_xml.py: Parse the xml format file to json format
* statistics.py: Count the number of verbs and noun pairs
  - Usage: python statistic.py [data path] [file name] [output dir]
  -File names: seperated by ',' for example: 01,02,03,04
* refine_data.py: find out the verb or noun pair with small number
  - Usage: python refine_data.py [data path] [output dir] [verb threshold] [noun threshold]
* delete_small.py: delete the verb and noun pair from the small list
* generate.py: generate the data for LDA

##### Author
I am a master student from National Taiwan University.

