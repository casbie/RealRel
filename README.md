RealRel
=======

Proposed Topic
===
To find out the relation between 2 pairs with given corpus

Proposed Method
===
1. cluster the noun pairs by LDA as groups, assuming each group present one relation
2. select the seed from the groups as training data
3. with the training data, learn the model to decide the relation between each pair

Files
===
* parse_xml.py: parse the xml format file to json format
* statistics.py: count the number of verbs and noun pairs
* refine_data.py: find out the verb or noun pair with small number
* delete_small.py: delete the verb and noun pair from the small list
* generate.py: generate the data for LDA

Author
===
I am a master student from National Taiwan University.

