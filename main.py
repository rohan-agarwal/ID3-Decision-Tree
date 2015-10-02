from functions import *


def main():
    input_file_name, training_set_size, number_of_trials, verbose = get_args()
    data = parse_txt(input_file_name)
    tree_accuracies = [0] * number_of_trials
    base_accuracies = [0] * number_of_trials

    for i in range(number_of_trials):
        print "\nTRIAL NUMBER: " + str(i+1) + "\n------------------------------------\n"
        train, test = train_test(data, training_set_size)
        names = train[0].keys()
        attributes = names[:len(names)-1]
        tree = id3(train, mode(train), attributes, 'root')
        print "Tree Structure: "
        print_tree_structure(tree)

        tree_accuracy, base_accuracy = tree_performance(tree, train, test)
        print "Tree accuracy: " + str(tree_accuracy)
        print "Base accuracy: " + str(base_accuracy)

        if verbose == 1:
            verbose_print(train, test, tree)

        tree_accuracies[i] = tree_accuracy
        base_accuracies[i] = base_accuracy

    print "Input file: " + str(input_file_name)
    print "Training set size: " + str(training_set_size)
    print "Testing set size: " + str(len(data) - training_set_size)
    print "Number of trials: " + str(number_of_trials)
    print "Average tree accuracy: " + str(sum(tree_accuracies)/len(tree_accuracies))
    print "Average base accuracy: " + str(sum(base_accuracies)/len(base_accuracies))

main()
