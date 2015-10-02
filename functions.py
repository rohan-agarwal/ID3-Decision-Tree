import sys
import csv
import random
import math


class Node:
    def __init__(self, attribute_name, parent):
        self.attribute_name = attribute_name
        self.parent = parent
        self.true_child = None
        self.false_child = None


def get_args():
    input_file_name = str(sys.argv[1])
    training_set_size = int(sys.argv[2])
    number_of_trials = int(sys.argv[3])
    verbose = int(sys.argv[4])

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


def train_test(data, training_set_size):
    shuffle = random.sample(data, len(data))
    train = shuffle[:training_set_size]
    test = shuffle[training_set_size:]

    return train, test


def mode(data):
    true_ct = sum([row['CLASS'] for row in data])
    if 2*true_ct >= len(data):
        return True
    return False


def ratios(data):
    true_ratio = float(sum([row['CLASS'] for row in data]))/float(len(data))
    false_ratio = 1 - true_ratio

    return true_ratio, false_ratio


def calculate_entropy(data):
    if len(data) == 0:
        return 0

    true_ratio, false_ratio = ratios(data)

    if true_ratio == 0:
        entropy = 0
    elif false_ratio == 0:
        entropy = 0
    else:
        entropy = -true_ratio * math.log(true_ratio, 2) - false_ratio * math.log(false_ratio, 2)

    return entropy


def data_split(data, attribute):
    true_data = [row for row in data if row[attribute] is True]
    false_data = [row for row in data if row[attribute] is False]

    return true_data, false_data


def calculate_gain(data, attribute, entropy_start):
    true_data, false_data = data_split(data, attribute)
    gain = entropy_start - \
        float(len(true_data))/float(len(data)) * calculate_entropy(true_data) - \
        float(len(false_data))/float(len(data)) * calculate_entropy(false_data)

    return gain


def find_best(attributes, data):
    if len(attributes) == 0:
        return None

    att = None
    max_gain = 0
    entropy = calculate_entropy(data)

    for var in attributes:
        gain = calculate_gain(data, var, entropy)
        if gain > max_gain:
            max_gain = gain
            att = var

    if att is not None:
        return att


def id3(data, default, attributes, parent):
    # Check for empty data
    if len(data) == 0:
        return default

    # Get prior probabilities
    prior_true, prior_false = ratios(data)

    # Check for all of the data being in one class
    if prior_true == 1:
        return True
    if prior_false == 1:
        return False

    # If there are no attributes, return the mode
    if len(attributes) == 0:
        return mode(data)

    # Find best attribute and create node
    best = find_best(attributes, data)
    if best is None:
        return mode(data)
    root = Node(best, parent)

    # Recurse to get subtrees
    best_true, best_false = data_split(data, best)
    attributes.remove(best)
    true_attributes = list(attributes)
    false_attributes = list(attributes)

    root.true_child = id3(best_true, mode(best_true), true_attributes, best)

    root.false_child = id3(best_false, mode(best_false), false_attributes, best)

    return root


def predict(tree, row):
    if tree is True:
        return True
    elif tree is False:
        return False
    elif row[tree.attribute_name] is True:
        return predict(tree.true_child, row)
    else:
        return predict(tree.false_child, row)


def match_prediction(tree, row):
    if predict(tree, row) == row['CLASS']:
        return True
    return False


def tree_performance(tree, train, test):

    tree_accuracy = float(sum([match_prediction(tree, row) for row in test]))/float(len(test))
    base_accuracy = float(
        len([row for row in test if row['CLASS'] == mode(train)]))/float(len(test))

    return tree_accuracy, base_accuracy


def print_tree_structure(root):
    if type(root.true_child) is bool and type(root.false_child) is bool:
        print "Attribute: " + str(root.attribute_name) + \
            "\nParent: " + str(root.parent) + \
            "\nTrue Child: " + str(root.true_child) + \
            "\nFalse Child: " + str(root.false_child) + "\n"
    elif type(root.true_child) is bool and type(root.false_child) is not bool:
        print "Attribute: " + str(root.attribute_name) + \
            "\nParent: " + str(root.parent) + \
            "\nTrue Child: " + str(root.true_child) + \
            "\nFalse Child: " + str(root.false_child.attribute_name) + "\n"
        print_tree_structure(root.false_child)
    elif type(root.true_child) is not bool and type(root.false_child) is bool:
        print "Attribute: " + str(root.attribute_name) + \
            "\nParent: " + str(root.parent) + \
            "\nTrue Child: " + str(root.true_child.attribute_name) + \
            "\nFalse Child: " + str(root.false_child) + "\n"
        print_tree_structure(root.true_child)
    elif type(root.true_child) is not bool and type(root.false_child) is not bool:
        print "Attribute: " + str(root.attribute_name) + \
            "\nParent: " + str(root.parent) + \
            "\nTrue Child: " + str(root.true_child.attribute_name) + \
            "\nFalse Child: " + str(root.false_child.attribute_name) + "\n"
        print_tree_structure(root.true_child)
        print_tree_structure(root.false_child)


def verbose_print(train, test, tree):
    print "Training Data:\n"
    for row in train:
        print row

    print "Testing Data:\n"
    for row in test:
        print row
        print "Tree Classification: " + str(predict(tree, row))
        print "Prior Classification: " + str(mode(train)) + "\n"
