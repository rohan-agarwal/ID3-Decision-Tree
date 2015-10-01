import sys
import csv
import random
import math


class Node:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        self.children = []

    def set_name(self, name):
        self.attribute_name = name

    def add_child(self, child):
        self.children.append(child)


def get_args():
    input_file_name = sys.argv[0]
    training_set_size = sys.argv[1]
    number_of_trials = sys.argv[2]
    verbose = sys.argv[3]

    return input_file_name, training_set_size, number_of_trials, verbose


def parse_booleans(data):
    for row in data:
        for item in row:
            if 'true' in row[item]:
                row[item] = True
            else:
                row[item] = False

    return data


def parse_txt(input_file_name):
    data = []
    with open(input_file_name) as datafile:
        reader = csv.DictReader(datafile, delimiter="\t")
        for row in reader:
            data.append(row)

    data = parse_booleans(data)

    return data


def data_split(data, training_set_size):
    shuffle = random.sample(data, len(data))
    train = shuffle[:training_set_size]
    test = shuffle[training_set_size:]

    return train, test


def ratios(data):
    true_ratio = float(sum([row['CLASS'] for row in data]))/float(len(data))
    false_ratio = 1 - true_ratio

    return true_ratio, false_ratio


def calculate_entropy(data):
    true_ratio, false_ratio = ratios(data)
    entropy = -true_ratio * math.log(true_ratio, 2) - false_ratio * math.log(false_ratio, 2)

    return entropy


def calculate_gain(data, attribute, entropy_start):
    true_data = [row for row in data if row[attribute] is True]
    false_data = [row for row in data if row[attribute] is False]
    gain = entropy_start - \
        float(len(true_data))/float(len(data)) * calculate_entropy(true_data) - \
        float(len(false_data))/float(len(data)) * calculate_entropy(false_data)

    return gain


def add_best(node, attributes, data):
    att = 0
    max_gain = 0
    entropy = calculate_entropy(data)

    for var in attributes:
        gain = calculate_gain(data, var, entropy)
        if gain > max_gain:
            max_gain = gain
            att = var

    new_node = Node(att)
    node.add_child(new_node)
    attributes.remove(att)
    add_best(new_node, attributes, data)


def id3(data, response, attributes):
    # Get prior probabilities
    prior_true, prior_false = ratios(data)

    # Create root
    root = Node('root')

    # Check for all of the data being in one class
    if prior_true == 1:
        root.add_child(True)
        return root
    if prior_false == 1:
        root.add_child(False)
        return root

    # If there are no attributes, return the root
    # Output is based on priors
    if len(attributes) == 0:
        if prior_true > prior_false:
            root.add_child(True)
            return root
        if prior_false > prior_true:
            root.add_child(False)
            return root



    return root_att
