def sort_data(input_file, output_file, index):
    import csv
    fp_in = open(input_file, 'r')
    fp_out = open(output_file, 'w')

    data = []

    for line in fp_in:
        single_data = line.strip().split(',')
        single_data[index] = int(single_data[index])
        data.append(single_data)

    data = sorted(data, key = lambda x : x[index], reverse = True)

    writer = csv.writer(fp_out)
    writer.writerows(data)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sort the data for given file')
    parser.add_argument('file_in', type=str, help='input file name')
    parser.add_argument('file_out', type=str, help='output file name')
    parser.add_argument('index', type=int, help='the column used for sort')
    
    args = parser.parse_args()
    
    input_file = args.file_in
    output_file = args.file_out
    index = args.index
    sort_data(input_file, output_file, index)


if __name__ == '__main__':
    main()
